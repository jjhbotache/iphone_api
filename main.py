#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import os
import sys
import sqlite3

# Add the current directory to Python's path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import BaseHTTPServer
from config import MAIN_DB_NAME, DATABASES_FOLDER, MEDIA_FOLDER, CREATE_DATABASES_TABLE, CREATE_MEDIA_TABLE
from database_api import DatabaseAPI

def initialize_main_database():
    conn = sqlite3.connect(MAIN_DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_DATABASES_TABLE)
    cursor.execute(CREATE_MEDIA_TABLE)
    conn.commit()
    conn.close()

def run_server(port=8000):
    server_address = ('', port)
    httpd = BaseHTTPServer.HTTPServer(server_address, DatabaseAPI)
    print ("Server running on port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(DATABASES_FOLDER):
        os.makedirs(DATABASES_FOLDER)
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
    initialize_main_database()
    run_server()