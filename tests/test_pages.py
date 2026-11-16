"""Build and fetch the public artifact under a project-site prefix."""
import functools
import http.server
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import threading
import unittest
from urllib.request import urlopen
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from library import build

class PagesTests(unittest.TestCase):
    def test_project_prefix_and_public_artifact(self):
        source=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('site','catalog','assets'):shutil.copytree(source/name,root/name)
            shutil.copyfile(source/'organization.json',root/'organization.json')
            build(root)
            public=root/'hosting';public.mkdir();shutil.move(root/'dist',public/'visual-shelf')
            artifact=public/'visual-shelf'
            self.assertRegex((artifact/'index.html').read_text(),r'app\.js\?v=[a-f0-9]{12}')
            self.assertTrue((artifact/'.nojekyll').exists())
            for name in ('.drafts','.exports','packages','retired','scripts','resources','catalog'):self.assertFalse((artifact/name).exists())
            class Handler(http.server.SimpleHTTPRequestHandler):
                def log_message(self,*args):pass
            server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(public)))
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            base=f'http://127.0.0.1:{server.server_port}/visual-shelf/'
            try:
                with urlopen(base) as res:html=res.read().decode()
                paths=re.findall(r'(?:src|href)="([^"#]+)"',html)
                paths += ['catalog.json','organization.json']
                for path in paths:
                    if path.startswith(('http:', 'https:')):continue
                    self.assertFalse(path.startswith('/'))
                    with urlopen(base+path) as res:self.assertEqual(res.status,200)
                records=json.loads((artifact/'catalog.json').read_text())
                for item in records:
                    with urlopen(base+item['path']) as res:self.assertGreater(len(res.read()),0)
            finally:
                server.shutdown();server.server_close();thread.join()
