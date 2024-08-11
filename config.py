#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os

# Database configuration
MAIN_DB_NAME = 'main_database.db'
DATABASES_FOLDER = os.path.join(os.path.dirname(__file__), 'databases')
MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), 'media')
with open('documentation.html', 'r') as file:
    DOCUMENTATION_HTML = file.read()

# API configuration
API_PASSWORD = 'J1234567890j'

# SQL for creating main database tables
CREATE_DATABASES_TABLE = '''
CREATE TABLE IF NOT EXISTS databases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,
    password TEXT NOT NULL
);
'''

CREATE_MEDIA_TABLE = '''
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,
    visibility_hidden BOOLEAN NOT NULL
);
'''