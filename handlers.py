# -*- coding: utf-8 -*-
from __future__ import with_statement
import sqlite3
import os
import tempfile
import shutil
import base64
import config
import utils

def handle_database_crud(self, method, data):
    if method == 'GET':
        databases = [f for f in os.listdir(config.DATABASES_FOLDER) if f.endswith('.db')]
        self.send_json_response(databases)
    elif method == 'POST':
        if 'name' not in data:
            self.send_json_response({"error": "Database name is required"}, 400)
            return
        db_name = data['name'] + '.db'
        db_path = os.path.join(config.DATABASES_FOLDER, db_name)
        if os.path.exists(db_path):
            self.send_json_response({"error": "Database already exists"}, 400)
            return
        conn = sqlite3.connect(db_path)
        conn.close()
        os.makedirs(os.path.join(config.MEDIA_FOLDER, data['name'] + '_MEDIA'))
        self.send_json_response({"message": "Database created successfully"})
    elif method == 'PUT':
        if 'name' not in data or 'new_name' not in data:
            self.send_json_response({"error": "Both 'name' and 'new_name' are required"}, 400)
            return
        old_db_name = data['name'] + '.db'
        new_db_name = data['new_name'] + '.db'
        old_db_path = os.path.join(config.DATABASES_FOLDER, old_db_name)
        new_db_path = os.path.join(config.DATABASES_FOLDER, new_db_name)
        old_media_path = os.path.join(config.MEDIA_FOLDER, data['name'] + '_MEDIA')
        new_media_path = os.path.join(config.MEDIA_FOLDER, data['new_name'] + '_MEDIA')
        
        if not os.path.exists(old_db_path):
            self.send_json_response({"error": "Database does not exist"}, 404)
            return
        if os.path.exists(new_db_path):
            self.send_json_response({"error": "New database name already exists"}, 400)
            return
        
        try:
            os.rename(old_db_path, new_db_path)
            if os.path.exists(old_media_path):
                os.rename(old_media_path, new_media_path)
            self.send_json_response({"message": "Database renamed successfully"})
        except OSError, e:
            self.send_json_response({"error": "Error renaming database: %s" % str(e)}, 500)
    elif method == 'DELETE':
        if 'name' not in data:
            self.send_json_response({"error": "Database name is required"}, 400)
            return
        db_name = data['name'] + '.db'
        db_path = os.path.join(config.DATABASES_FOLDER, db_name)
        media_path = os.path.join(config.MEDIA_FOLDER, data['name'] + '_MEDIA')
        
        if not os.path.exists(db_path):
            self.send_json_response({"error": "Database does not exist"}, 404)
            return
        
        try:
            os.remove(db_path)
            if os.path.exists(media_path):
                shutil.rmtree(media_path)
            self.send_json_response({"message": "Database deleted successfully"})
        except OSError, e:
            self.send_json_response({"error": "Error deleting database: %s" % str(e)}, 500)
    else:
        self.send_json_response({"error": "Method not allowed"}, 405)
        
def handle_crud(self, method, path_parts, data, database):
    db_path = os.path.join(config.DATABASES_FOLDER, database)
    if not os.path.exists(db_path):
        self.send_json_response({"error": "Database not found"}, 404)
        return

    table = path_parts[0] if path_parts else None
    id = path_parts[1] if len(path_parts) > 1 else None

    conn = sqlite3.connect(db_path)
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
                    self.send_json_response({"error": "Not Found"}, 404)
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
            self.send_json_response({"id": cursor.lastrowid})

        elif method == 'PUT':
            if not id:
                self.send_json_response({"error": "ID required for PUT"}, 400)
                return
            set_clause = ', '.join(["%s = ?" % key for key in data.keys()])
            values = tuple(data.values()) + (id,)
            cursor.execute("UPDATE %s SET %s WHERE id = ?" % (table, set_clause), values)
            conn.commit()
            self.send_json_response({"updated": cursor.rowcount})

        elif method == 'DELETE':
            if not id:
                self.send_json_response({"error": "ID required for DELETE"}, 400)
                return
            cursor.execute("DELETE FROM %s WHERE id = ?" % table, (id,))
            conn.commit()
            self.send_json_response({"deleted": cursor.rowcount})

    except sqlite3.Error, e:
        self.send_json_response({"error": str(e)}, 500)
    finally:
        conn.close()

def handle_import(self, data, database):
    if 'file' not in data:
        self.send_json_response({"error": "No file provided"}, 400)
        return

    file_data = data['file']

    try:
        file_data = utils.add_padding(file_data)
        decoded_file_data = base64.b64decode(file_data)
    except (TypeError, base64.binascii.Error), e:
        self.send_json_response({"error": "Base64 decoding error: %s" % str(e)}, 400)
        return

    db_path = os.path.join(config.DATABASES_FOLDER, database)
    temp_file_path = tempfile.mktemp()
    try:
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(decoded_file_data)
        
        shutil.copy(temp_file_path, db_path)
        self.send_json_response({'message': 'Database imported successfully'})
    except IOError, e:
        self.send_json_response({"error": "Error copying database: %s" % str(e)}, 500)
    finally:
        os.unlink(temp_file_path)

def handle_export(self, database):
    db_path = os.path.join(config.DATABASES_FOLDER, database)
    if not os.path.exists(db_path):
        self.send_json_response({"error": "Database not found"}, 404)
        return

    try:
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Content-Disposition', 'attachment; filename="%s"' % database)
        self.end_headers()

        with open(db_path, 'rb') as f:
            self.wfile.write(f.read())
    except IOError, e:
        self.send_json_response({"error": "Error reading database file: %s" % str(e)}, 500)

def handle_media(self, method, path_parts, data, database):
    media_folder = os.path.join(config.MEDIA_FOLDER, database.split('.')[0] + '_MEDIA')
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    file_name = path_parts[0] if path_parts else None

    if method == 'GET':
        if file_name:
            utils.get_file(self, file_name, media_folder)
        else:
            utils.list_files(self, media_folder)
    elif method == 'POST':
        utils.upload_file(self, file_name, data, media_folder)
    elif method == 'DELETE':
        utils.delete_file(self, file_name, media_folder)
    else:
        self.send_json_response({"error": "Method Not Allowed"}, 405)

def handle_query(self, data, database):
    if 'query' not in data:
        self.send_json_response({"error": "No query provided"}, 400)
        return

    query = data['query']
    
    if not query.lower().startswith('select'):
        self.send_json_response({"error": "Only SELECT queries are allowed"}, 400)
        return

    db_path = os.path.join(config.DATABASES_FOLDER, database)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        self.send_json_response(result)
    except sqlite3.Error, e:
        self.send_json_response({"error": str(e)}, 500)
    finally:
        conn.close()

def handle_execute(self, data, database):
    if 'query' not in data:
        self.send_json_response({"error": "No query provided"}, 400)
        return

    query = data['query']
    
    if query.lower().startswith('select'):
        self.send_json_response({"error": "Use /api/query for SELECT statements"}, 400)
        return

    db_path = os.path.join(config.DATABASES_FOLDER, database)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        conn.commit()
        self.send_json_response({"affected_rows": cursor.rowcount})
    except sqlite3.Error, e:
        conn.rollback()
        self.send_json_response({"error": str(e)}, 500)
    finally:
        conn.close()

def serve_documentation(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    html = config.DOCUMENTATION_HTML
    self.wfile.write(html)