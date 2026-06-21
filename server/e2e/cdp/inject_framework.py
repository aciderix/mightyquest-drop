import requests, websocket, json, time, re, os, posixpath
ROOT="/home/user/port/GameData/Data"
HTML=os.path.join(ROOT,"UI/Html/en/Index.html")
BASEDIR="/UI/Html/en"
def resolve(ref): return os.path.join(ROOT, posixpath.normpath(posixpath.join(BASEDIR,ref)).lstrip("/"))
html=open(HTML,encoding="utf-8",errors="replace").read()
srcs=re.findall(r'<script[^>]*\bsrc="([^"]+)"', html)
print("scripts in Index.html:", len(srcs))
def page0():
    for x in requests.get("http://localhost:9222/json",timeout=5).json():
        if x.get('type')=='page': return x
p=page0(); print("page url:", p.get('url'))
ws=websocket.create_connection(p['webSocketDebuggerUrl'],timeout=15,suppress_origin=True)
i=[0]
def cmd(method,params=None):
    i[0]+=1; mid=i[0]
    ws.send(json.dumps({"id":mid,"method":method,"params":params or {}}))
    while True:
        m=json.loads(ws.recv())
        if m.get("id")==mid: return m
def ev(expr):
    r=cmd("Runtime.evaluate",{"expression":expr,"returnByValue":True})
    res=r.get("result",{})
    if "exceptionDetails" in res or res.get("wasThrown"):
        return "THREW:"+json.dumps(res.get("result",{}).get("description",res))[:120]
    return res.get("result",{}).get("value")
cmd("Runtime.enable")
print("before: typeof hyperquest =", ev("typeof hyperquest"))
ok=0; fail=0; firstfails=[]
for s in srcs:
    fp=resolve(s)
    try: code=open(fp,encoding="utf-8",errors="replace").read()
    except Exception as e: fail+=1; continue
    r=cmd("Runtime.evaluate",{"expression":code,"returnByValue":False})
    res=r.get("result",{})
    if "exceptionDetails" in res or res.get("wasThrown"):
        fail+=1
        if len(firstfails)<6:
            d=res.get("result",{}).get("description") or res.get("exceptionDetails")
            firstfails.append((os.path.basename(s), str(d)[:100]))
    else: ok+=1
print("injected ok=%d fail=%d"%(ok,fail))
for n,d in firstfails: print("  FAIL", n, d)
print("after: typeof hyperquest =", ev("typeof hyperquest"))
print("hyperquest.client?", ev("typeof hyperquest!=='undefined' && typeof hyperquest.client"))
print("Facade?", ev("typeof Facade"))
print("controllers:", ev("typeof hyperquest!=='undefined'&&hyperquest.controller?Object.keys(hyperquest.controller):'none'"))
ws.close()
