#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver

import os

PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()