#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import os
import sys

# Add the current directory to Python's path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import BaseHTTPServer
from config import DB_NAME, MEDIA_FOLDER, DATABASES_FOLDER
from database_api import DatabaseAPI

def run_server(port=8000):
    server_address = ('', port)
    httpd = BaseHTTPServer.HTTPServer(server_address, DatabaseAPI)
    print "Server running on port", port
    httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
    if not os.path.exists(DATABASES_FOLDER):
        os.makedirs(DATABASES_FOLDER)
    run_server()