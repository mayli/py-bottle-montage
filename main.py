#!/usr/bin/env python
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

def download(urls, prefix):
    names = []
    for url in urls:
        name = os.path.join(prefix, os.path.basename(url))
        with open(name, 'wb') as f:
            f.write(session.get(url).content)
        names.append(name)
    return names

@get('/')
def get_index():
    return "montage api: " + open('/proc/loadavg').read()

@post('/montage')
def montage_handler():
    urls = request.json()
    dtemp = tempfile.mkdtemp()
    names = download(urls, dtemp)
    output = os.path.join(dtemp)
    check_call(['montage'] + names + ['-frame', '5', '-geometry', '+1+1', output])
    content = open(output, 'rb').read()
    shutil.rmtree(dtemp)
    response.set_header('Content-type', 'image/jpeg')
    return content

if __name__ == '__main__':
    bottle.run(host = '0.0.0.0', port = 8080)
