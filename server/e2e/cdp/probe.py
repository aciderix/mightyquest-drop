import requests, websocket, json, sys
pages=requests.get("http://localhost:9222/json",timeout=5).json()
print("targets:", [(p.get('type'),p.get('url')) for p in pages])
def ev(ws_url, expr):
    ws=websocket.create_connection(ws_url, timeout=8, suppress_origin=True)
    ws.send(json.dumps({"id":1,"method":"Runtime.evaluate",
        "params":{"expression":expr,"returnByValue":True}}))
    for _ in range(20):
        m=json.loads(ws.recv())
        if m.get("id")==1:
            ws.close(); return m
    ws.close(); return {"timeout":True}
for p in pages:
    if p.get('type')!='page': continue
    u=p['webSocketDebuggerUrl']
    print("\n=== page %s url=%s ==="%(p['id'][:8], p.get('url')))
    for expr in ["1+1","document.location.href","typeof hyperquest","document.title","document.documentElement?document.documentElement.outerHTML.length:'NO_DOC'"]:
        try:
            r=ev(u,expr)
            res=r.get("result",{}).get("result",{})
            print("  %-55s -> %s"%(expr, res.get("value", res)))
        except Exception as e:
            print("  %-55s -> ERR %s"%(expr,e))
