# -*- coding: utf-8 -*-
from __future__ import with_statement
import BaseHTTPServer
import urlparse
import cgi
import handlers
import utils
import os

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
        if not self.check_permission():
            return

        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
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

        database = self.headers.getheader('Database')
        if not database and path not in ['/', '/api/databases']:
            self.send_json_response({"error": "Database header is required"}, 400)
            return

        if path == '/':
            handlers.serve_documentation(self)
        elif path == '/api/databases':
            handlers.handle_database_crud(self, method, data)
        elif path.startswith('/api/crud/'):
            handlers.handle_crud(self, method, path.split('/')[3:], data, database)
        elif path == '/api/import':
            handlers.handle_import(self, data, database)
        elif path == '/api/export':
            handlers.handle_export(self, database)
        elif path.startswith('/api/media') or path.startswith('/api/media/'):
            handlers.handle_media(self, method, path.split('/')[3:], data, database)
        elif path == '/api/query':
            handlers.handle_query(self, data, database)
        elif path == '/api/execute':
            handlers.handle_execute(self, data, database)
        else:
            self.send_json_response({"error": "Not Found"}, 404)

    def check_permission(self):
        if self.path.startswith('/api/media/') and self.command == 'GET' or self.path.startswith('/'):
            return True
        code = self.headers.getheader('Code')
        if code != '040800':
            self.send_json_response({"error": "Permission denied"}, 403)
            return False
        return True

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(utils.dumps(data))