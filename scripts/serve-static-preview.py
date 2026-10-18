"""Preview only public files under a project path, without the Node server."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--port',type=int,default=17888)
parser.add_argument('--prefix',default='/moments-studio/')
args=parser.parse_args()
prefix='/'+args.prefix.strip('/')+'/' if args.prefix.strip('/') else '/'
public=Path(__file__).resolve().parent.parent/'public'
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(public),**kw)
 def do_GET(self):
  path=urlsplit(self.path).path
  if not path.startswith(prefix):self.send_error(404);return
  self.path='/'+self.path[len(prefix):]
  super().do_GET()
 def log_message(self,*a):pass
print(f'Static preview: http://127.0.0.1:{args.port}{prefix}',flush=True)
ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
