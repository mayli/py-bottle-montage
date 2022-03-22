#!/usr/bin/env python3
try:
    import eventlet; eventlet.monkey_patch()
except ImportError:
    pass

import tempfile
import os
import shutil
from subprocess import check_call
import bottle
import requests


from bottle import request, response
from bottle import post, get

session = requests.Session()
app = application = bottle.default_app()

def download(url, prefix):
    name = os.path.join(prefix, os.path.basename(url))
    with open(name, 'wb') as f:
        resp = session.get(url)
        resp.raise_for_status()
        f.write(resp.content)
    return name

def download_func(arg):
    return download(*arg)

def download_urls(urls, prefix):
    pool = eventlet.GreenPool()
    names = list(pool.imap(download_func, [(url, prefix) for url in urls]))
    return names

@get('/')
def get_index():
    with open('/proc/loadavg') as f:
        return "montage api: " + f.read()

@post('/montage')
def montage_handler():
    urls = request.json
    print(' '.join(urls))
    dtemp = tempfile.mkdtemp()
    names = download_urls(urls, dtemp)
    output = os.path.join(dtemp, 'frame.jpg')
    check_call(['montage'] + names + ['-font', 'Liberation-Mono', '-frame', '5', '-geometry', '+1+1', output])
    with open(output, 'rb') as f:
        content = f.read()
    shutil.rmtree(dtemp)
    response.set_header('Content-type', 'image/jpeg')
    return content

if __name__ == '__main__':
    port = os.environ.get("PORT", 8080)
    port = int(port)
    bottle.run(server='eventlet', host = '0.0.0.0', port = port, debug=True)
