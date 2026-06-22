#!/usr/bin/env python3
"""
stub_server.py — community-server stub for The Mighty Quest for Epic Loot.

Iteration 3: routes on the REAL endpoint pattern observed in live traffic
(`/<Service>Service.hqs/<Method>`, see re/catalog/network/endpoints_observed.txt)
and answers with COMPLETE, correctly-typed responses generated from the reversed
catalog (re/catalog/network/generated/examples.json — full field sets, real enum
values, `$type` discriminators). Stateful accounts/sessions, persisted. Logs
every request so unknown calls are easy to fill in.

Zero dependencies (Python 3 stdlib). Run on the game machine or a VPS:
    python3 server/stub_server.py --host 0.0.0.0 --port 8080
"""
from __future__ import annotations
import argparse, copy, datetime, json, os, re, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from completeness_gate import Gate
from command_notifications import CommandBus
from gameplay_catalog import catalog

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
NET = os.path.join(ROOT, "re/catalog/network")
EXAMPLES = json.load(open(os.path.join(NET, "generated/examples.json"))) \
    if os.path.exists(os.path.join(NET, "generated/examples.json")) else {}
GATE = Gate()            # schema-completeness for every response we emit
BUS = CommandBus(GATE)   # SendCommands -> correct notifications
PKG_VERSIONS = json.load(open(os.path.join(NET, "package_versions.json"))) \
    if os.path.exists(os.path.join(NET, "package_versions.json")) else {}
STATE_PATH = os.path.join(HERE, "state.json")
LOG_PATH = os.path.join(HERE, "requests.log")


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def envelope(payload):
    """Wrap a contract in the game's real response envelope. Confirmed against our
    captured real traffic (real_traffic.log): reads -> {"Result": <contract>};
    things that emit notifications -> {"Notifications": [...]} (and EndAttack uses
    both). Already-enveloped or empty payloads pass through untouched."""
    if not payload:
        return {}
    if isinstance(payload, dict) and (
            payload.keys() & {"Result", "Notifications", "GlobalNotifications"}):
        return payload
    return {"Result": payload}


UNCERTAIN_PATH = os.path.join(HERE, "uncertain.log")


def contract(name, **overrides):
    """A SCHEMA-COMPLETE `name`: starts from the catalog example, applies overrides,
    then runs the completeness gate so every field the client expects is present and
    nested contracts are filled (not left as {} -> silent client defaults).

    Any value we are NOT certain about (an enum resolved only by heuristic, or an
    enum name we could not resolve) is appended to uncertain.log with the contract
    and field — so if something misbehaves in game, you can grep this for the
    suspect field instead of hunting blind."""
    seed = copy.deepcopy(EXAMPLES.get(name, {}))
    seed.update(overrides)
    if name not in GATE.schemas:
        return seed
    uncertain = []
    obj = GATE.complete(name, seed, uncertain=uncertain)
    if uncertain:
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(UNCERTAIN_PATH, "a") as f:
            for u in uncertain:
                f.write(f"{ts} {name}: {u}\n")
    return obj


# ---- persistent state ------------------------------------------------------
class State:
    def __init__(self, path):
        self.path = path; self.lock = threading.Lock()
        self.data = {"accounts": {}, "sessions": {}, "next_id": 1}
        if os.path.exists(path):
            try: self.data.update(json.load(open(path)))
            except Exception: pass

    def save(self):
        json.dump(self.data, open(self.path + ".tmp", "w"), indent=1)
        os.replace(self.path + ".tmp", self.path)

    def login(self, identity):
        with self.lock:
            acc = self.data["accounts"].get(identity)
            if not acc:
                aid = self.data["next_id"]; self.data["next_id"] += 1
                acc = {"AccountId": aid, "DisplayName": "", "Privileges": 9,
                       # the loot economy lives here, persisted across requests
                       "wallet": {"InGameCoin": 0, "LifeForce": 0, "PremiumCash": 0,
                                  "InGameCoinStorageCapacity": 100000,
                                  "LifeForceStorageCapacity": 100000},
                       "items": [], "next_item": 1}
                self.data["accounts"][identity] = acc
            token = f"tok-{acc['AccountId']}-{os.urandom(4).hex()}"
            self.data["sessions"][token] = acc["AccountId"]
            self.save(); return acc, token

    def account(self, token):
        aid = self.data["sessions"].get(token)
        return next((a for a in self.data["accounts"].values() if a["AccountId"] == aid), None)

    def award(self, acc, gold=0, lifeforce=0, item_template=None):
        """Apply attack rewards to an account and persist them."""
        with self.lock:
            acc.setdefault("wallet", {"InGameCoin": 0, "LifeForce": 0, "PremiumCash": 0,
                                      "InGameCoinStorageCapacity": 100000,
                                      "LifeForceStorageCapacity": 100000})
            acc["wallet"]["InGameCoin"] += gold
            acc["wallet"]["LifeForce"] += lifeforce
            new_item = None
            if item_template is not None:
                iid = acc.get("next_item", 1); acc["next_item"] = iid + 1
                new_item = {"ExpirableId": f"item-{iid}", "TemplateId": item_template,
                            "AcquisitionDate": now(), "SellPrice": 50}
                acc.setdefault("items", []).append(new_item)
            self.save(); return new_item


STATE = State(STATE_PATH)


# ---- game endpoints (/<Service>Service.hqs/<Method>) ------------------------
def ep_account_information(req, acc):
    # Privileges must be 9 for a new account or hero-selection never shows.
    acc = acc or {}
    wallet = acc.get("wallet", {"InGameCoin": 0, "LifeForce": 0, "PremiumCash": 0,
                                "InGameCoinStorageCapacity": 100000,
                                "LifeForceStorageCapacity": 100000})
    inv = contract("AccountInventory")
    inv["HeroItems"] = acc.get("items", [])      # reflect looted items
    return contract("AccountInformation", AccountId=acc.get("AccountId", 1),
                    DisplayName=acc.get("DisplayName", ""), Privileges=9,
                    Wallet=wallet, Inventory=inv)


def ep_choose_display_name(req, acc):
    name = (req.json.get("displayName") or req.json.get("DisplayName") or "Player")
    if acc:
        acc["DisplayName"] = name; STATE.save()
    return contract("AccountSummary", AccountId=(acc or {}).get("AccountId", 1), DisplayName=name)


CAT = catalog()
_LVL_RE = re.compile(r"PVE_(\d+)_")


def _castle_level(name):
    m = _LVL_RE.search(name or "")
    return max(1, int(m.group(1))) if m else 1


def ep_start_attack(req, acc):
    """Serve a REAL castle from the decrypted catalog (default: first tutorial
    castle) so combat gets real rooms, creature placement and tiers -- not an
    empty skeleton. The real lists are set AFTER the gate so it cannot clobber
    them back to []."""
    body = req.json or {}
    cid = body.get("CastleId") or body.get("castleId")
    if not (cid and CAT.has("Castles", cid)):
        cid = CAT.find_one("Castles", "PVE_00_TUTORIAL_01")
    cas = CAT.get("Castles", cid)
    name = CAT.name("Castles", cid)
    level = _castle_level(name)

    castle = contract("Castle",
                      AccountId=cas.get("AccountId", 2),
                      AccountDisplayName=name,
                      LayoutId=cas.get("LayoutId", 1),
                      ThemeId=cas.get("ThemeId", 0),
                      OasisNameId=cas.get("OasisName", 0))
    # real content, kept verbatim from the catalog (post-gate so it survives)
    castle["Rooms"] = cas.get("Rooms", [])
    castle["CreatureTiers"] = cas.get("CreatureTiers", [])
    castle["TrapTiers"] = cas.get("TrapTiers", [])

    ai = contract("AttackInfo",
                  Level=level,
                  CastleHeartRank=max(1, level // 5),
                  AdjustedHeroLevel=level,
                  IsTutorial=bool(cas.get("IsTutorialCastle")))
    ai["Castle"] = castle
    return ai


def ep_end_attack(req, acc):
    """The loot loop: a won attack pays gold + life force and drops one item.
    Returns the reward notifications the real server emits (Wallet + inventory)."""
    body = req.json or {}
    won = body.get("victory", body.get("Victory", True)) and \
          body.get("completionType", "TreasureRoom") != "Escape"
    if not (acc and won):
        return {}
    item = STATE.award(acc, gold=100, lifeforce=25, item_template=1001)
    notifs = [
        contract("WalletUpdatedNotification", Index=0, NotificationType=24, Amounts=[
            {"Amount": 100, "CurrencyType": 2},    # IGC (gold)
            {"Amount": 25,  "CurrencyType": 4}]),  # LifeForce
        contract("HeroInventoryAddedNotification", Index=1, NewlyAdded=item),
    ]
    return {"Notifications": notifs}


# method name -> handler(req, acc) ; default below serves a matching example
ENDPOINTS = {
    "GetAccountInformation": ep_account_information,
    "ChooseDisplayName":     ep_choose_display_name,
    "GetAttackSelectionList": lambda r, a: contract("AttackSelectionResult"),
    "GetCastleInfo":          lambda r, a: contract("CastleInfo"),
    "StartAttack":            ep_start_attack,
    "EndAttack":              ep_end_attack,
    "GetCastlesForSale":      lambda r, a: contract("CastlesForSaleSelectionResult"),
    "ChooseFirstHero":        lambda r, a: {},          # response contract TBD
    "SendCommands":           lambda r, a: BUS.handle(r.json),  # command bus -> notifications
    "CheckSeasonalCompetitionRewards": lambda r, a: {},
}

# boot / launcher-side endpoints (the local proxy / distribution layer)
def boot_config(req):
    return contract("BootConfig", DistributionServiceUrl=req.base, GameWebsiteUrl=req.base,
                    EnvironmentName="community", WorldName="community")


def distribution(req):
    # echo the client package versions so the patch-check passes
    return PKG_VERSIONS or {}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    @property
    def base(self):
        h = self.headers.get("Host") or f"{self.server.server_address[0]}:{self.server.server_address[1]}"
        return f"http://{h}"

    def token(self):
        a = self.headers.get("Authorization", "")
        return a[7:] if a.lower().startswith("bearer ") else self.headers.get("X-Connection-Token")

    def _read(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        try: self._json = json.loads(body) if body else {}
        except Exception: self._json = {}
        return body

    @property
    def json(self): return self._json

    def _log(self, body):
        line = f"{now()} {self.command} {self.path} len={len(body)}"
        print(line)
        with open(LOG_PATH, "a") as f:
            f.write(line + ("\n    " + body[:1500].decode("latin1", "replace") if body else "") + "\n")

    def _send(self, obj, code=200):
        p = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(p)))
        self.end_headers(); self.wfile.write(p)

    def _handle(self):
        body = self._read(); self._log(body)
        path = self.path.split("?")[0]
        # game RPC: /<Service>Service.hqs/<Method>
        m = re.match(r"/([A-Za-z]+)Service\.hqs/([A-Za-z]+)", path)
        if m:
            service, method = m.group(1), m.group(2)
            acc = STATE.account(self.token())
            if acc is None:
                acc, _ = STATE.login(self.headers.get("X-Steam-Ticket", "anonymous"))
            h = ENDPOINTS.get(method)
            return self._send(envelope(h(self, acc) if h else self._guess(method)))
        low = path.lower()
        if "login" in low or "account" in low and "creation" in low:
            acc, token = STATE.login(self.json.get("steamticket", "anonymous"))
            return self._send(contract("LoginResult", AccountId=acc["AccountId"],
                                        ConnectionToken=token, ProfileId=str(acc["AccountId"])))
        if "bootconfig" in low:
            return self._send(boot_config(self))
        if "package" in low or "distribution" in low or "version" in low:
            return self._send(distribution(self))
        # fall back: serve an example matching the last path segment
        seg = os.path.splitext(path.rstrip("/").split("/")[-1])[0]
        return self._send(EXAMPLES.get(seg, {}))

    def _guess(self, method):
        """no handler: serve an example whose contract name appears in the method."""
        for c in EXAMPLES:
            if c.lower() in method.lower():
                return EXAMPLES[c]
        return {}

    do_GET = do_POST = do_PUT = _handle

    def log_message(self, *a): pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--tls", action="store_true",
                    help="serve HTTPS using the MQEL CA/server cert (for the game's "
                         "curl, which needs TLS on :443 to gs.themightyquest.com)")
    ap.add_argument("--cert"); ap.add_argument("--key")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    scheme = "http"
    if a.tls:
        import ssl
        cert, key = a.cert, a.key
        if not (cert and key):
            # reuse the launcher's two-level PKI so the game (and ca.pem) trust us
            import mqel_launcher as L
            cert, key, _ = L.ensure_certs()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        ctx.minimum_version = ssl.TLSVersion.TLSv1     # 2013 client
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
        scheme = "https"
    print(f"[+] MQEL stub on {scheme}://{a.host}:{a.port}  ({len(EXAMPLES)} contract examples)")
    print(f"[+] stateful routing /<Service>Service.hqs/<Method>; state {STATE_PATH}; log {LOG_PATH}")
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\n[+] stopped")


if __name__ == "__main__":
    main()
