# -*- coding: utf-8 -*-
from __future__ import with_statement
import os
import config
import utils

def add_padding(data):
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    return data

def dumps(obj):
    if isinstance(obj, dict):
        return '{' + ','.join(['"' + str(k) + '":' + dumps(v) for k, v in obj.items()]) + '}'
    elif isinstance(obj, list):
        return '[' + ','.join([dumps(i) for i in obj]) + ']'
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif isinstance(obj, (int, long, float)):
        return str(obj)
    elif isinstance(obj, (str, unicode)):
        return '"' + obj.replace('"', '\\"') + '"'
    elif obj is None:
        return 'null'
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")

def loads(s):
    return eval(s, {"true": True, "false": False, "null": None})
  
  
# media functions
def list_files(self):
  try:
      files = os.listdir(config.MEDIA_FOLDER)
      self.send_json_response(files)
  except IOError , e:
            self.send_error(500, "Error reading media directory: %s" % str(e))

def get_file(self, file_name):
    file_path = os.path.join(config.MEDIA_FOLDER, file_name)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
        except IOError , e:
            self.send_error(500, "Error reading file: %s" % str(e))
    else:
        self.send_error(404, "File not found")

def upload_file(self, file_name, data):
    if 'file' not in data:
        self.send_error(400, "No file provided")
        return

    file_data = data['file']
    file_data = utils.add_padding(file_data)

    try:
        decoded_file_data = base64.b64decode(file_data)
    except Exception , e:
        self.send_error(400, "Invalid base64 encoding")
        return

    file_path = os.path.join(config.MEDIA_FOLDER, file_name)

    try:
        with open(file_path, 'wb') as f:
            f.write(decoded_file_data)
        
        self.send_json_response({"message": "File uploaded successfully"})
    except IOError , e:
        self.send_error(500, "Error writing file: %s" % str(e))

def delete_file(self, file_name):
        file_path = os.path.join(config.MEDIA_FOLDER, file_name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                self.send_json_response({"message": "File deleted successfully"})
            except IOError , e:
                self.send_error(500, "Error deleting file: %s" % str(e))
        else:
            self.send_error(404, "File not found")