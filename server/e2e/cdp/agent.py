#!/usr/bin/env python3
"""
cdp/agent.py — drive The Mighty Quest's CEF (Chromium-28) webview from Python
over the Chrome DevTools Protocol.

Why this exists
---------------
The game's lobby is an HTML/JS app (the `hyperquest` framework) rendered in an
embedded CEF browser. Launch the client with `--remote-debugging-port=9222`
(see ../launch_lobby.sh) and this agent attaches to the webview's V8 context and
becomes the bot-control layer the project set out to build: read UI state, call
`hyperquest.controller.*`, drive flows — all from Python over a WebSocket.

Two modes
---------
* attach()         — attach to the live game webview (real Windows / Wine+GPU host
                     where the page actually loads and the native `manager._proxy`
                     bridge is bound). This is the "control the real game" mode.
* bootstrap_local()— in a headless container the CEF renderer does NOT load pages
                     and the native bridge is never bound (about:blank, no
                     `manager`). This mode injects a mock DOM, the full hyperquest
                     framework, and a *Python-transported* `manager._proxy`: JS
                     calls are captured here, forwarded to our local game server,
                     and the responses fed back via `hyperquest.client.invokeResponse`.
                     It turns the injected framework into a headless client whose
                     transport is Python — useful to exercise the server and script
                     flows even where Chromium's own networking is broken under Wine.

Robustness (per the CDP-under-Wine gotchas we measured)
* hit the HTTP `/json` endpoint EXACTLY once, then keep the WebSocket open for the
  whole session (the old debug HTTP server wedges after heavy use);
* one long-lived process — never re-discover targets mid-session.

Deps: websocket-client, requests  (pip install websocket-client requests)
"""
from __future__ import annotations
import json, os, posixpath, re, sys, time
import requests, websocket

GAME_DATA = os.environ.get("MQ_GAMEDATA", "/home/user/port/GameData/Data")
HTML_DIR  = "/UI/Html/en"
SERVER    = os.environ.get("MQ_SERVER", "https://127.0.0.1")
CDP_HOST  = os.environ.get("MQ_CDP", "http://localhost:9222")


def _resolve(ref: str) -> str:
    return os.path.join(GAME_DATA, posixpath.normpath(posixpath.join(HTML_DIR, ref)).lstrip("/"))


class Agent:
    def __init__(self, target_index: int = 0):
        # Step 1: ONE /json, then keep the socket forever.
        pages = requests.get(f"{CDP_HOST}/json", timeout=8).json()
        self.targets = [p for p in pages if p.get("type") == "page"]
        if not self.targets:
            raise RuntimeError("no CEF page targets on the debug port")
        self.page = self.targets[target_index]
        self.ws = websocket.create_connection(
            self.page["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self._id = 0
        self.cmd("Runtime.enable")

    # ── raw CDP ──────────────────────────────────────────────────────────────
    def cmd(self, method, params=None):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == mid:
                return m

    def eval(self, expr, by_value=True):
        r = self.cmd("Runtime.evaluate",
                     {"expression": expr, "returnByValue": by_value}).get("result", {})
        if r.get("wasThrown") or "exceptionDetails" in r:
            desc = r.get("result", {}).get("description") or r.get("exceptionDetails")
            raise RuntimeError("JS threw: %s" % str(desc)[:300])
        return r.get("result", {}).get("value")

    # ── high level ───────────────────────────────────────────────────────────
    def has_native_bridge(self) -> bool:
        return self.eval("typeof window.manager!=='undefined' && !!window.manager._proxy") is True

    def inject_dom(self):
        """Step 2 — give the framework the DOM it expects (the real <body>)."""
        html = open(os.path.join(GAME_DATA, "UI/Html/en/Index.html"),
                    encoding="utf-8", errors="replace").read()
        m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
        body = m.group(1) if m else "<div id='main-lobby-panel'></div>"
        doc = "<html><head></head><body>" + body + "</body></html>"
        self.eval("document.open();document.write(%s);document.close();1" % json.dumps(doc))
        return self.eval("!!document.getElementById('main-lobby-panel')")

    def inject_framework(self):
        """Load every <script src> from Index.html, in order, into V8."""
        html = open(os.path.join(GAME_DATA, "UI/Html/en/Index.html"),
                    encoding="utf-8", errors="replace").read()
        srcs = re.findall(r'<script[^>]*\bsrc="([^"]+)"', html)
        ok = fails = 0
        failures = []
        for s in srcs:
            try:
                code = open(_resolve(s), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            r = self.cmd("Runtime.evaluate",
                         {"expression": code, "returnByValue": False}).get("result", {})
            if r.get("wasThrown"):
                fails += 1
                if len(failures) < 10:
                    failures.append((os.path.basename(s),
                                     str(r.get("result", {}).get("description"))[:160]))
            else:
                ok += 1
        return {"ok": ok, "fail": fails, "failures": failures,
                "hyperquest": self.eval("typeof hyperquest")}

    def install_python_bridge(self, methods):
        """Mock `manager._proxy` (no native bridge under headless Wine, and
        Chromium's own networking is broken there). Every JS->native call is
        queued on window.__mq_calls; pump() drains it, forwards to the real game
        server, and feeds the answer back through hyperquest.client.invokeResponse.
        `methods` = iterable of API method names the proxy must expose."""
        js_methods = ",".join(
            "%s:function(a){window.__mq_calls.push({m:%s,a:a,rid:hyperquest.client._lastRequestId});}"
            % (json.dumps(m)[1:-1] if False else m, json.dumps(m)) for m in methods)
        # build proxy object with explicit methods (Chromium 28 has no ES6 Proxy)
        body = ";".join(
            "P[%s]=function(a){window.__mq_calls.push({m:%s,a:a,rid:hyperquest.client._lastRequestId});}"
            % (json.dumps(m), json.dumps(m)) for m in methods)
        self.eval("window.__mq_calls=[];var P={};%s;window.manager={_proxy:P};1" % body)

    def pump(self, route):
        """Drain queued JS->native calls; `route(method, arg)->response_obj`."""
        calls = self.eval("var c=window.__mq_calls;window.__mq_calls=[];c") or []
        for c in calls:
            resp = route(c.get("m"), c.get("a"))
            self.eval("hyperquest.client.invokeResponse(%d,%s);1"
                      % (int(c.get("rid", 0)), json.dumps(resp)))
        return len(calls)


def _server_route(method, arg):
    """Forward a captured proxy call to the local game server over HTTP."""
    # the proxy method name maps onto /<Service>Service.hqs/<Method>; we don't
    # know the service split here, so callers usually supply their own route().
    import urllib.request, ssl
    ctx = ssl.create_default_context(); ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    data = json.dumps(arg or {}).encode()
    # best-effort: try AccountService then ServerCommandService
    for svc in ("Account", "ServerCommand", "Castle", "Attack"):
        try:
            req = urllib.request.Request(f"{SERVER}/{svc}Service.hqs/{method}",
                                         data=data, method="POST")
            return json.loads(urllib.request.urlopen(req, timeout=5, context=ctx).read() or b"{}")
        except Exception:
            continue
    return {}


def main():
    a = Agent()
    print("attached:", a.page.get("url"))
    native = a.has_native_bridge()
    print("native manager._proxy bridge present:", native)
    if native:
        # real host: framework already running in the page; just drive it.
        print("hyperquest:", a.eval("typeof hyperquest"))
        print("controllers:", a.eval(
            "typeof hyperquest!=='undefined'&&hyperquest.controller?Object.keys(hyperquest.controller):'n/a'"))
        return
    # headless/local mode
    print("inject_dom main-lobby-panel:", a.inject_dom())
    info = a.inject_framework()
    print("inject_framework:", {k: info[k] for k in ("ok", "fail", "hyperquest")})
    for n, d in info["failures"]:
        print("   FAIL", n, "::", d)
    # expose the server methods on the mock proxy and do one pump
    methods = ["GetAccountInformation", "SendCommands", "GetCastleInfo",
               "ChooseDisplayName", "GetAttackSelectionList"]
    a.install_python_bridge(methods)
    # drive one call end to end through Python transport
    a.eval("hyperquest.client._lastRequestId++;hyperquest.client._mapCallback[hyperquest.client._lastRequestId]="
           "{functionToCall:function(r){window.__last_account=r;}};"
           "manager._proxy.GetAccountInformation({});1")
    n = a.pump(_server_route)
    print("pumped %d call(s)" % n)
    print("account response seen in JS:",
          a.eval("window.__last_account?Object.keys(window.__last_account).slice(0,8):'none'"))


if __name__ == "__main__":
    main()
