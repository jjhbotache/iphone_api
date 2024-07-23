# -*- coding: utf-8 -*-
from __future__ import with_statement
import sqlite3
import os
import tempfile
import shutil
import base64
import config
import utils

def handle_crud(self, method, path_parts, data):
    table = path_parts[0] if path_parts else None
    id = path_parts[1] if len(path_parts) > 1 else None

    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    try:
        if method == 'GET':
            if id:
                cursor.execute("SELECT * FROM %s WHERE id = ?" % table, (id,))
                row = cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    self.send_json_response(dict(zip(columns, row)))
                else:
                    self.send_error(404, "Not Found")
            else:
                cursor.execute("SELECT * FROM %s" % table)
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                self.send_json_response([dict(zip(columns, row)) for row in rows])

        elif method == 'POST':
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = tuple(data.values())
            cursor.execute("INSERT INTO %s (%s) VALUES (%s)" % (table, columns, placeholders), values)
            conn.commit()
            self.send_json_response({"id": cursor.lastrowid}, 201)

        elif method == 'PUT':
            if not id:
                self.send_error(400, "ID required for PUT")
                return
            set_clause = ', '.join(["%s = ?" % key for key in data.keys()])
            values = tuple(data.values()) + (id,)
            cursor.execute("UPDATE %s SET %s WHERE id = ?" % (table, set_clause), values)
            conn.commit()
            self.send_json_response({"updated": cursor.rowcount})

        elif method == 'DELETE':
            if not id:
                self.send_error(400, "ID required for DELETE")
                return
            cursor.execute("DELETE FROM %s WHERE id = ?" % table, (id,))
            conn.commit()
            self.send_json_response({"deleted": cursor.rowcount})

    except sqlite3.Error , e:
        self.send_error(500, str(e))
    finally:
        conn.close()

def handle_import(self, data):
    if 'file' not in data:
        self.send_error(400, "No file provided")
        return

    file_data = data['file']

    try:
        file_data = utils.add_padding(file_data)
        decoded_file_data = base64.b64decode(file_data)
    except (TypeError, base64.binascii.Error), e:
        self.send_error(400, "Base64 decoding error: %s" % str(e))
        return

    temp_file_path = tempfile.mktemp()
    try:
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(decoded_file_data)
        
        shutil.copy(temp_file_path, config.DB_NAME)
        self.send_json_response({'message': 'Database imported successfully'})
    except IOError, e:
        self.send_error(500, "Error copying database: %s" % str(e))
    finally:
        os.unlink(temp_file_path)

def handle_export(self):
    if not os.path.exists(config.DB_NAME):
        self.send_error(404, "Database not found")
        return

    try:
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Content-Disposition', 'attachment; filename="database_export.sqlite"')
        self.end_headers()

        with open(config.DB_NAME, 'rb') as f:
            self.wfile.write(f.read())
    except IOError, e:
        self.send_error(500, "Error reading database file: %s" % str(e))

def handle_media(self, method, path_parts, data):
    file_name = path_parts[0] if path_parts else None

    if method == 'GET':
        if file_name:
            utils.get_file(self,file_name)
        else:
            utils.list_files(self)
    elif method == 'POST':
        utils.upload_file(self,file_name, data)
    elif method == 'DELETE':
        utils.delete_file(self,file_name)
    else:
        self.send_error(405, "Method Not Allowed")

def serve_documentation(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    html = config.DOCUMENTATION_HTML
    self.wfile.write(html)
    
def handle_query(self, data):
    if 'query' not in data:
        self.send_error(400, "No query provided")
        return

    query = data['query']
    
    if not query.lower().startswith('select'):
        self.send_error(400, "Only SELECT queries are allowed")
        return

    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        self.send_json_response(result)
    except sqlite3.Error , e:
        self.send_error(500, str(e))
    finally:
        conn.close()

def handle_execute(self, data):
    if 'query' not in data:
        self.send_error(400, "No query provided")
        return

    query = data['query']
    
    
    if query.lower().startswith('select'):
        self.send_error(400, "Use /api/query for SELECT statements")
        return

    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        conn.commit()
        self.send_json_response({"affected_rows": cursor.rowcount})
    except sqlite3.Error , e:
        conn.rollback()
        self.send_error(500, str(e))
    finally:
        conn.close()