#!/usr/bin/env python3
# Serves GameData/Data under /gamedata/. For the webview HTML pages it INLINES
# every <script src> and <link rel=stylesheet> (resolved on disk) into the one
# document, because CEF (Chromium 28) under Wine fails to load sub-resources.
import os,re,sys,posixpath
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
ROOT="/home/user/port/GameData/Data"
import urllib.parse

def resolve(base_url_dir, ref):
    # base_url_dir like /UI/Html/en ; ref like ../../Js/x.js -> disk path
    p=posixpath.normpath(posixpath.join(base_url_dir, ref))
    return os.path.join(ROOT, p.lstrip("/"))

def inline_html(disk_path, url_path):
    html=open(disk_path,encoding="utf-8",errors="replace").read()
    html=html.replace("<head>","<head><script>throw new Error('PROBE_INLINE_RAN')</script>",1)
    base_dir=posixpath.dirname(url_path)  # e.g. /gamedata/UI/Html/en
    base_dir=base_dir[len("/gamedata"):] if base_dir.startswith("/gamedata") else base_dir
    def script_sub(m):
        src=m.group(1)
        fp=resolve(base_dir, src)
        try:
            code=open(fp,encoding="utf-8",errors="replace").read()
            return "<script type=\"text/javascript\">\n"+code+"\n</script>"
        except Exception as e:
            return "<!-- inline-fail script %s -->"%src
    def link_sub(m):
        href=m.group(1)
        fp=resolve(base_dir, href)
        try:
            css=open(fp,encoding="utf-8",errors="replace").read()
            return "<style type=\"text/css\">\n"+css+"\n</style>"
        except Exception:
            return "<!-- inline-fail css %s -->"%href
    html=re.sub(r'<script[^>]*\bsrc="([^"]+)"[^>]*>\s*</script>', script_sub, html)
    html=re.sub(r'<link[^>]*\bhref="([^"]+)"[^>]*rel="stylesheet"[^>]*/?>', link_sub, html)
    html=re.sub(r'<link[^>]*rel="stylesheet"[^>]*\bhref="([^"]+)"[^>]*/?>', link_sub, html)
    return b"\xef\xbb\xbf"+html.encode("utf-8")

class H(BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"
    def do_GET(self):
        path=urllib.parse.urlparse(self.path).path
        if not path.startswith("/gamedata/"):
            self.send_error(404); return
        rel=path[len("/gamedata/"):]
        disk=os.path.join(ROOT, rel)
        if not os.path.isfile(disk):
            self.send_error(404); return
        if disk.lower().endswith(".html") or disk.lower().endswith(".htm"):
            body=inline_html(disk, path)
            ctype="text/html; charset=utf-8"
        else:
            body=open(disk,"rb").read()
            ext=os.path.splitext(disk)[1].lower()
            ctype={"js":"application/javascript","css":"text/css","png":"image/png",
                   "jpg":"image/jpeg","gif":"image/gif","json":"application/json",
                   "woff":"font/woff","ttf":"font/ttf"}.get(ext.lstrip("."),"application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type",ctype)
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()
        try: self.wfile.write(body)
        except Exception: pass
    def log_message(self,*a):
        sys.stderr.write("UI %s %s\n"%(self.command,self.path)); sys.stderr.flush()

if __name__=="__main__":
    ThreadingHTTPServer(("127.0.0.1",80),H).serve_forever()
