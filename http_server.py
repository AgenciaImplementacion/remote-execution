#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver

import os

# para new_list_directory
import urllib.parse
import html
import sys
import io
from http import HTTPStatus

PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler

# https://gist.github.com/touilleMan/eb02ea40b93e52604938
Handler.extensions_map.update({
    '.log': 'text/plain',
})

# https://github.com/python/cpython/blob/3.6/Lib/http/server.py
def new_list_directory(self, path):
    """Helper to produce a directory listing (absent index.html).
    Return value is either a file object, or None (indicating an
    error).  In either case, the headers are sent, making the
    interface the same as for send_head().
    """
    try:
        list = os.listdir(path)
    except OSError:
        self.send_error(
            HTTPStatus.NOT_FOUND,
            "No permission to list directory")
        return None
    list.sort(key=lambda a: a.lower(), reverse=True)
    r = []
    try:
        displaypath = urllib.parse.unquote(self.path,
                                           errors='surrogatepass')
    except UnicodeDecodeError:
        displaypath = urllib.parse.unquote(path)
    displaypath = html.escape(displaypath, quote=False)
    enc = sys.getfilesystemencoding()
    title = 'Mostrando log %s' % displaypath
    r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
             '"http://www.w3.org/TR/html4/strict.dtd">')
    r.append('<html>\n<head>')
    r.append('<meta http-equiv="Content-Type" '
             'content="text/html; charset=%s">' % enc)
    r.append('<title>%s</title>\n</head>' % title)
    r.append('<body>\n<h1>%s</h1>' % title)
    r.append('<hr>\n<ul>')
    for name in list:
        fullname = os.path.join(path, name)
        displayname = linkname = name
        # Append / for directories or @ for symbolic links
        if os.path.isdir(fullname):
            displayname = name + "/"
            linkname = name + "/"
        if os.path.islink(fullname):
            displayname = name + "@"
            # Note: a link to a directory displays with @ and links with /
        r.append('<li><a href="%s">%s</a></li>'
                 % (urllib.parse.quote(linkname,
                                       errors='surrogatepass'),
                    html.escape(displayname, quote=False)))
    r.append('</ul>\n<hr>\n')
    r.append('Copyright &copy;&nbsp;2017 Diseñado y Desarrollado por <a href="http://proadmintierra.info/">Agencia de Implementación Swissphoto-Incige</a>. Todos los Derechos Reservados.')
    r.append('</body>\n</html>\n')
    encoded = '\n'.join(r).encode(enc, 'surrogateescape')
    f = io.BytesIO()
    f.write(encoded)
    f.seek(0)
    self.send_response(HTTPStatus.OK)
    self.send_header("Content-type", "text/html; charset=%s" % enc)
    self.send_header("Content-Length", str(len(encoded)))
    self.end_headers()
    return f

def get_state():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.log')]
    #print('files', files)
    #print('file[-5:-1]', [file[-4:] for file in files])
    if len(files) == 0:
        return 'unknown.svg'
    files = sorted(files)
    last_file = files[-1]
    print('Last log file: ' + last_file)
    if last_file.endswith('__error.log'):
        return 'failing.svg'
    elif last_file.endswith('__success.log'):
        return 'passing.svg'
    else:
        return 'unknown.svg'
    
def get_text_image_state():
    file = open(os.path.abspath(os.path.join('../templates', get_state())), 'r')
    body = file.read().encode('UTF-8', 'replace')
    file.close()
    return body
    
# https://github.com/python/cpython/blob/3.6/Lib/http/server.py#L634
def new_do_GET(self):
    """Serve a GET request only for STATUS."""
    if self.path == '/status.svg':
        print('Returning ', self.path)
        import datetime
        import base64
        #r = []
        #r.append('<html></html>')
        #body = '\n'.join(r).encode('UTF-8', 'replace')
        body = get_text_image_state()
        f = io.BytesIO()
        f.write(body)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "image/svg+xml; charset=UTF-8")
        self.send_header("Cache-control", "no-cache, private")
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
        expires = expires.strftime('%a, %d %b %Y %H:%M:%S GTM')
        self.send_header("Expires", expires)
        encoded = base64.b64encode(expires.encode())
        self.send_header("Etag", '"{hash}"'.format(hash=str(encoded.decode())))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.copyfile(f, self.wfile)
        finally:
            f.close()
        return
    """Default!!!"""
    """Serve a GET request."""
    f = self.send_head()
    if f:
        try:
            self.copyfile(f, self.wfile)
        finally:
            f.close()

Handler.do_GET = new_do_GET			
Handler.list_directory = new_list_directory

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
