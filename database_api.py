#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import BaseHTTPServer
import urlparse
import cgi
import handlers
import utils
import os
import config

class DatabaseAPI(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def handle_request(self, method):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        
        if (not self.give_right_password()) and (path != '/'):
            self.send_json_response({"error": "Permission denied"}, 403)
            return

        query = cgi.parse_qs(parsed_path.query)
        content_length = int(self.headers.getheader('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            body = utils.loads(body) if body else None
        else:
            body = None

        data = query.copy()
        if isinstance(body, dict):
            data.update(body)

        if path == '/':
            handlers.serve_documentation(self)
        elif path.startswith('/db/'):
            self.handle_db_request(method, path, data)
        elif path.startswith('/media/'):
            self.handle_media_request(method, path, data)
        else:
            self.send_json_response({"error": "Not Found"}, 404)

    def give_right_password(self):
        api_password = self.headers.getheader('Api-Password')
        if api_password != config.API_PASSWORD:
            return False
        return True

    def handle_db_request(self, method, path, data):
        if path not in ['/db/create', '/db/list']:
            database = self.headers.getheader('Database')
            database_password = self.headers.getheader('Database-Password')
            
            if not database or not database_password:
                self.send_json_response({"error": "Database and Database-Password headers are required"}, 400)
                return

            if not handlers.check_database_permission(database, database_password):
                self.send_json_response({"error": "Invalid database credentials"}, 403)
                return
        else:
            database = None  # No se necesita para /db/create y /db/list
        
        if path == '/db/query':
            handlers.handle_query(self, data, database)
        elif path == '/db/execute':
            handlers.handle_execute(self, data, database)
        elif path == '/db/import':
            handlers.handle_import(self, data, database)
        elif path == '/db/export':
            handlers.handle_export(self, database)
        elif path == '/db/delete':
            handlers.handle_delete_database(self, database)
        elif path == '/db/create':
            handlers.handle_create_database(self, data)
        elif path == '/db/list':
            handlers.handle_list_databases(self)
        else:
            self.send_json_response({"error": "Not Found"}, 404)

    def handle_media_request(self, method, path, data):
        parts = path.split('/')
        if len(parts) != 5:
            self.send_json_response({"error": "Invalid media path"}, 400)
            return

        _, database_name, db_password, media_name = parts[1:]

        if not handlers.check_database_permission(database_name, db_password):
            self.send_json_response({"error": "Invalid database credentials"}, 403)
            return

        if method == 'GET':
            handlers.handle_media_get(self, database_name, media_name)
        elif method == 'POST':
            handlers.handle_media_post(self, database_name, media_name, data)
        elif method == 'DELETE':
            handlers.handle_media_delete(self, database_name, media_name)
        else:
            self.send_json_response({"error": "Method not allowed"}, 405)

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(utils.dumps(data))