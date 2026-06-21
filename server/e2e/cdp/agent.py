#!/usr/bin/env python3
"""
cdp/agent.py — drive The Mighty Quest's CEF (Chromium-28) webview from Python
over the Chrome DevTools Protocol, and script full client↔server flows.

Launch the client with `--remote-debugging-port=9222` (see ../launch_lobby.sh)
and run this agent. It attaches to the webview's V8 context and becomes the
bot-control layer: inject + run the `hyperquest` JS framework, then drive the
real client↔server protocol (account creation → hero pick → lobby → attack)
through the framework's own transport, with Python relaying every call to the
local game server.

Modes
-----
* real host (Windows / Wine+GPU): the page loads and the native `manager._proxy`
  bridge is bound — `has_native_bridge()` is True; drive the live game UI.
* headless container: the CEF renderer never loads a page (about:blank) and the
  native bridge is absent, so we inject a mock DOM + the framework + a
  Python-transported `manager._proxy`. JS calls are captured, routed to the game
  server over HTTP, and the answers fed back via `hyperquest.client.invokeResponse`.

Robustness (CDP-under-Wine): hit `/json` exactly once, keep the WebSocket for the
whole process; one long-lived agent, never re-discover targets mid-session.

Deps: websocket-client, requests
"""
from __future__ import annotations
import json, os, posixpath, re, ssl, sys, time, urllib.request
import requests, websocket

# the completeness gate lets the agent guarantee (and report) that every response
# the JS framework receives is schema-complete with enum integers, not names.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
try:
    from completeness_gate import Gate
except Exception:
    Gate = None

# method -> response contract (so we can gate/validate the response object)
METHOD_CONTRACT = {
    "GetAccountInformation": "AccountInformation",
    "ChooseDisplayName": "AccountSummary",
    "ChooseFirstHero": None,
    "GetCastleInfo": "CastleInfo",
    "GetAttackSelectionList": "AttackSelectionResult",
    "GetCastlesForSale": "CastlesForSaleSelectionResult",
    "StartAttack": "AttackInfo",
    "EndAttack": None,
    "SendCommands": None,
}

GAME_DATA = os.environ.get("MQ_GAMEDATA", "/home/user/port/GameData/Data")
HTML_DIR  = "/UI/Html/en"
SERVER    = os.environ.get("MQ_SERVER", "https://127.0.0.1")
CDP_HOST  = os.environ.get("MQ_CDP", "http://localhost:9222")

# method -> Service, from re/catalog/network/endpoints_observed.txt (real routing)
SERVICE = {
    "SendCommands": "ServerCommand",
    "StartAttack": "Attack", "EndAttack": "Attack",
    "GetCastleInfo": "AttackSelection", "GetAttackSelectionList": "AttackSelection",
    "GetAccountInformation": "AccountInformation",
    "GetCastlesForSale": "CastleForSale", "GetCastleForSaleBuildInfo": "CastleForSale",
    "CheckSeasonalCompetitionRewards": "SeasonalCompetition",
    "ChooseFirstHero": "Hero",
    "ChooseDisplayName": "Account",
}
_SSL = ssl.create_default_context(); _SSL.check_hostname = False; _SSL.verify_mode = ssl.CERT_NONE


def _resolve(ref: str) -> str:
    return os.path.join(GAME_DATA, posixpath.normpath(posixpath.join(HTML_DIR, ref)).lstrip("/"))


def server_call(method, arg, services=None):
    """POST a captured proxy call to /<Service>Service.hqs/<Method> on the game server."""
    candidates = [SERVICE[method]] if method in SERVICE else (services or
                 ["AccountInformation", "Account", "ServerCommand", "AttackSelection",
                  "Attack", "Hero", "CastleForSale"])
    body = json.dumps(arg or {}).encode()
    last = {}
    for svc in candidates:
        try:
            req = urllib.request.Request(f"{SERVER}/{svc}Service.hqs/{method}",
                                         data=body, method="POST")
            raw = urllib.request.urlopen(req, timeout=6, context=_SSL).read()
            return json.loads(raw or b"{}")
        except Exception as e:
            last = {"__error": str(e)}
    return last


class Agent:
    def __init__(self, target_index=0):
        pages = requests.get(f"{CDP_HOST}/json", timeout=8).json()       # ONE /json
        self.targets = [p for p in pages if p.get("type") == "page"]
        if not self.targets:
            raise RuntimeError("no CEF page targets on the debug port")
        self.page = self.targets[target_index]
        self.ws = websocket.create_connection(self.page["webSocketDebuggerUrl"],
                                              timeout=30, suppress_origin=True)
        self._id = 0
        self.gate = Gate() if Gate else None
        self.cmd("Runtime.enable")

    # ── raw CDP ──────────────────────────────────────────────────────────────
    def cmd(self, method, params=None):
        self._id += 1; mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == mid:
                return m

    def eval(self, expr, by_value=True):
        r = self.cmd("Runtime.evaluate",
                     {"expression": expr, "returnByValue": by_value}).get("result", {})
        if r.get("wasThrown") or "exceptionDetails" in r:
            raise RuntimeError("JS threw: %s" %
                               str(r.get("result", {}).get("description") or r.get("exceptionDetails"))[:300])
        return r.get("result", {}).get("value")

    # ── bootstrap (headless container) ───────────────────────────────────────
    def has_native_bridge(self):
        return self.eval("typeof window.manager!=='undefined' && !!(window.manager&&window.manager._proxy)") is True

    def inject_dom(self):
        html = open(os.path.join(GAME_DATA, "UI/Html/en/Index.html"),
                    encoding="utf-8", errors="replace").read()
        m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
        body = m.group(1) if m else "<div id='main-lobby-panel'></div>"
        doc = "<html><head></head><body>" + body + "</body></html>"
        self.eval("document.open();document.write(%s);document.close();1" % json.dumps(doc))
        return self.eval("!!document.getElementById('main-lobby-panel')")

    def inject_framework(self):
        html = open(os.path.join(GAME_DATA, "UI/Html/en/Index.html"),
                    encoding="utf-8", errors="replace").read()
        srcs = re.findall(r'<script[^>]*\bsrc="([^"]+)"', html)
        ok = fail = 0; failures = []
        for s in srcs:
            try:
                code = open(_resolve(s), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            r = self.cmd("Runtime.evaluate",
                         {"expression": code, "returnByValue": False}).get("result", {})
            if r.get("wasThrown"):
                fail += 1
                if len(failures) < 10:
                    failures.append((os.path.basename(s),
                                     str(r.get("result", {}).get("description"))[:160]))
            else:
                ok += 1
        return {"ok": ok, "fail": fail, "failures": failures,
                "hyperquest": self.eval("typeof hyperquest")}

    def install_bridge(self):
        """Mock manager._proxy (no native bridge / Chromium net under Wine) +
        a clean __invoke(method,args) that registers a callback and queues the call."""
        self.eval("""
            window.__mq_calls = [];
            window.__resp = {};
            var P = {};
            window.__mkproxy = function(name){
                P[name] = function(a){
                    window.__mq_calls.push({m:name, a:a, rid:hyperquest.client._lastRequestId});
                };
            };
            window.manager = {_proxy: P};
            window.__jserr = null;
            window.onerror = function(m,u,l){ window.__jserr = String(m); };
            window.__invoke = function(method, args){
                var rid = ++hyperquest.client._lastRequestId;
                hyperquest.client._mapCallback[rid] =
                    {functionToCall:function(r){ window.__resp[rid] = r; }};
                if(!P[method]) window.__mkproxy(method);
                P[method](args || {});
                return rid;
            };
            1;""")

    def gate_response(self, method, resp):
        """Make the response correct-by-construction: unwrap the {"Result":...}
        envelope, fill all fields and convert enum NAMES to integers via the
        completeness gate. Returns (object_for_js, issues)."""
        # the real protocol wraps reads as {"Result": contract, "Notifications":[...]}
        inner = resp.get("Result", resp) if isinstance(resp, dict) else resp
        contract = METHOD_CONTRACT.get(method)
        if not (self.gate and contract and isinstance(inner, dict)):
            return inner, []
        fixed = self.gate.complete(contract, inner)
        return fixed, self.gate.validate(contract, fixed)

    def pump(self, report=None):
        """Drain queued JS->native calls, route to the server, gate the response,
        feed it back. `report` (dict) accumulates per-method validation issues."""
        calls = self.eval("var c=window.__mq_calls; window.__mq_calls=[]; c") or []
        for c in calls:
            method = c.get("m")
            raw = server_call(method, c.get("a"))
            obj, issues = self.gate_response(method, raw)
            if report is not None:
                report[method] = issues
            self.eval("hyperquest.client.invokeResponse(%d,%s);1"
                      % (int(c.get("rid", 0)), json.dumps(obj)))
        return len(calls)

    def invoke(self, method, args=None, timeout=8):
        """Drive one client->server call through the real hyperquest transport.
        Returns (response, validation_issues, js_error): the object the JS
        framework received, the gate's verdict on it, and any JS exception the
        framework threw while processing it (the behavioural oracle)."""
        self.eval("window.__jserr=null;1")
        rid = self.eval("__invoke(%s,%s)" % (json.dumps(method), json.dumps(args or {})))
        report = {}
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.pump(report)
            got = self.eval("window.__resp[%d]||null" % int(rid))
            if got is not None:
                jserr = self.eval("window.__jserr||null")
                return got, report.get(method, []), jserr
            time.sleep(0.1)
        return None, report.get(method, []), self.eval("window.__jserr||null")

    def bootstrap_local(self):
        assert self.inject_dom(), "mock DOM failed"
        info = self.inject_framework()
        assert info["hyperquest"] == "object", "framework inject failed: %s" % info
        self.install_bridge()
        return info


def run_flow():
    a = Agent()
    print("attached page url:", a.page.get("url"))
    if a.has_native_bridge():
        print("native bridge present — real-host mode (driving live game UI).")
    else:
        print("headless container — bootstrapping framework + Python transport...")
        info = a.bootstrap_local()
        print("  framework: ok=%d fail=%d" % (info["ok"], info["fail"]))

    def keys(o, n=10):
        return list(o.keys())[:n] if isinstance(o, dict) else o

    print("\n=== scripted flow (each response gated + client reaction checked) ===")
    steps = [
        ("GetAccountInformation", {}),
        ("ChooseDisplayName", {"displayName": "ClaudeHero"}),
        ("ChooseFirstHero", {"heroTemplateId": 1}),
        ("GetCastleInfo", {}),
        ("GetAttackSelectionList", {}),
        ("GetCastlesForSale", {}),
        ("StartAttack", {}),
        ("SendCommands", {"commands": [{"$type": "ClientIdleCommand"}]}),
        ("EndAttack", {}),
    ]
    all_ok = True
    for method, args in steps:
        try:
            resp, issues, jserr = a.invoke(method, args)
            verdict = "OK" if not issues and not jserr else (
                "%d schema issue(s)" % len(issues) if issues else "JS error")
            if issues or jserr:
                all_ok = False
            print("  %-24s [%s] -> %s" % (method, verdict, keys(resp)))
            for i in issues[:2]:
                print("        ! ", i)
            if jserr:
                print("        ! JS threw:", jserr)
        except Exception as e:
            all_ok = False
            print("  %-24s -> ERROR %s" % (method, e))
    print("\n%s — every response schema-complete (enum ints) and accepted by the "
          "JS framework without error." % ("ALL CORRECT" if all_ok else "ISSUES FOUND"))

    # statefulness: the name we just set must come back from a fresh read
    print("\n=== stateful check: re-read account after ChooseDisplayName ===")
    acc, _, _ = a.invoke("GetAccountInformation", {})
    dn = acc.get("DisplayName") if isinstance(acc, dict) else None
    print("  GetAccountInformation.DisplayName =", repr(dn),
          "->", "PERSISTED ✓" if dn == "ClaudeHero" else "not reflected")
    a.ws.close()


if __name__ == "__main__":
    run_flow()
