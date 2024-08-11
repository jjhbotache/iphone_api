#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import sqlite3
import os
import base64
import shutil
import config
import utils

def check_database_permission(database, password):
    conn = sqlite3.connect(config.MAIN_DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM databases WHERE path = ? AND password = ?", (database, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

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
        self.send_json_response({"error": "Use /db/query for SELECT statements"}, 400)
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

def handle_import(self, data, database):
    if 'file' not in data:
        self.send_json_response({"error": "No file provided"}, 400)
        return

    file_data = data['file']
    file_data = utils.add_padding(file_data)

    try:
        decoded_file_data = base64.b64decode(file_data)
    except Exception, e:
        self.send_json_response({"error": "Invalid base64 encoding"}, 400)
        return

    db_path = os.path.join(config.DATABASES_FOLDER, database)

    try:
        with open(db_path, 'wb') as f:
            f.write(decoded_file_data)
        
        self.send_json_response({"message": "Database imported successfully"})
    except IOError, e:
        self.send_json_response({"error": "Error writing file: %s" % str(e)}, 500)

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

def handle_delete_database(self, database):
    db_path = os.path.join(config.DATABASES_FOLDER, database)
    if not os.path.exists(db_path):
        self.send_json_response({"error": "Database not found"}, 404)
        return

    try:
        os.remove(db_path)
        conn = sqlite3.connect(config.MAIN_DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM databases WHERE path = ?", (database,))
        conn.commit()
        conn.close()
        self.send_json_response({"message": "Database deleted successfully"})
    except Exception, e:
        self.send_json_response({"error": "Error deleting database: %s" % str(e)}, 500)

def handle_create_database(self, data):
    if 'name' not in data or 'password' not in data:
        self.send_json_response({"error": "Name and password are required"}, 400)
        return

    db_name = data['name'] + '.db'
    db_path = os.path.join(config.DATABASES_FOLDER, db_name)
    
    if os.path.exists(db_path):
        self.send_json_response({"error": "Database already exists"}, 400)
        return

    try:
        conn = sqlite3.connect(db_path)
        conn.close()
        
        main_conn = sqlite3.connect(config.MAIN_DB_NAME)
        main_cursor = main_conn.cursor()
        main_cursor.execute("INSERT INTO databases (path, password) VALUES (?, ?)", (db_name, data['password']))
        main_conn.commit()
        main_conn.close()
        
        self.send_json_response({"message": "Database created successfully"})
    except Exception, e:
        self.send_json_response({"error": "Error creating database: %s" % str(e)}, 500)

def handle_list_databases(self):
    try:
        conn = sqlite3.connect(config.MAIN_DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM databases")
        databases = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.send_json_response(databases)
    except Exception, e:
        self.send_json_response({"error": str(e)}, 500)

def handle_media_get(self, database_name, media_name):
    media_path = os.path.join(config.MEDIA_FOLDER, database_name, media_name)
    if not os.path.exists(media_path):
        self.send_json_response({"error": "File not found"}, 404)
        return

    try:
        with open(media_path, 'rb') as f:
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(f.read())
    except IOError, e:
        self.send_json_response({"error": "Error reading file: %s" % str(e)}, 500)

def handle_media_post(self, database_name, media_name, data):
    if 'base64' not in data or 'visibility_hidden' not in data:
        self.send_json_response({"error": "base64 and visibility_hidden are required"}, 400)
        return

    file_data = data['base64']
    visibility_hidden = data['visibility_hidden']

    try:
        decoded_file_data = base64.b64decode(file_data)
    except Exception, e:
        self.send_json_response({"error": "Invalid base64 encoding"}, 400)
        return

    media_folder = os.path.join(config.MEDIA_FOLDER, database_name)
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    media_path = os.path.join(media_folder, media_name)

    try:
        with open(media_path, 'wb') as f:
            f.write(decoded_file_data)
        
        conn = sqlite3.connect(config.MAIN_DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO media (path, visibility_hidden) VALUES (?, ?)", 
                       (os.path.join(database_name, media_name), visibility_hidden))
        conn.commit()
        conn.close()

        self.send_json_response({"message": "File uploaded successfully"})
    except Exception, e:
        self.send_json_response({"error": "Error uploading file: %s" % str(e)}, 500)

def handle_media_delete(self, database_name, media_name):
    media_path = os.path.join(config.MEDIA_FOLDER, database_name, media_name)
    if not os.path.exists(media_path):
        self.send_json_response({"error": "File not found"}, 404)
        return

    try:
        os.remove(media_path)
        conn = sqlite3.connect(config.MAIN_DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM media WHERE path = ?", (os.path.join(database_name, media_name),))
        conn.commit()
        conn.close()
        self.send_json_response({"message": "File deleted successfully"})
    except Exception, e:
        self.send_json_response({"error": "Error deleting file: %s" % str(e)}, 500)

def serve_documentation(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    html = config.DOCUMENTATION_HTML
    self.wfile.write(html)