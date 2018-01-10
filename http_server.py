#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver

import os

PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler

# https://gist.github.com/touilleMan/eb02ea40b93e52604938
Handler.extensions_map.update({
    '.log': 'text/plain',
});

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
	list.sort(key=lambda a: a.lower())
	r = []
	try:
		displaypath = urllib.parse.unquote(self.path,
										   errors='surrogatepass')
	except UnicodeDecodeError:
		displaypath = urllib.parse.unquote(path)
	displaypath = html.escape(displaypath, quote=False)
	enc = sys.getfilesystemencoding()
	title = 'Directory listing for %s' % displaypath
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
	r.append('</ul>\n<hr>\n</body>\n</html>\n')
	encoded = '\n'.join(r).encode(enc, 'surrogateescape')
	f = io.BytesIO()
	f.write(encoded)
	f.seek(0)
	self.send_response(HTTPStatus.OK)
	self.send_header("Content-type", "text/html; charset=%s" % enc)
	self.send_header("Content-Length", str(len(encoded)))
	self.end_headers()
	return f
	

Handler.list_directory = new_list_directory

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()