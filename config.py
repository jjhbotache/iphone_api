# -*- coding: utf-8 -*-
import os

# Database configuration
DB_NAME = 'database.db'
DATABASES_FOLDER = os.path.join(os.path.dirname(__file__), 'databases')
MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), 'media')
DOCUMENTATION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }
        h1, h2 { color: #333; }
        details { margin-bottom: 20px; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
        summary { cursor: pointer; font-weight: bold; margin-bottom: 10px; }
        code { background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; display: block; white-space: pre-wrap; }
        .endpoint { margin-bottom: 20px; }
        .method { font-weight: bold; color: #0066cc; }
        .url { color: #009900; }
    </style>
</head>
<body>
    <h1>API Documentation</h1>

    <h2>General Information</h2>
    <p>Base URL: <code>http://your-api-base-url.com/api</code></p>
    <p>All requests should include the following headers:</p>
    <code>
Content-Type: application/json
Code: 040800
Database: your_database_name.db (except for /api/databases endpoint)
    </code>

    <details>
        <summary>Database Operations</summary>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/api/databases</span></h3>
            <p>List all databases</p>
            <h4>Example request:</h4>
            <code>
curl -X GET \
  http://your-api-base-url.com/api/databases \
  -H 'Code: 040800'
            </code>
            <h4>Example response:</h4>
            <code>
["database1.db", "database2.db", "database3.db"]
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/api/databases</span></h3>
            <p>Create a new database</p>
            <h4>Example request:</h4>
            <code>
curl -X POST \
  http://your-api-base-url.com/api/databases \
  -H 'Code: 040800' \
  -H 'Content-Type: application/json' \
  -d '{"name": "new_database"}'
            </code>
            <h4>Example response:</h4>
            <code>
{"message": "Database created successfully"}
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">PUT</span> <span class="url">/api/databases</span></h3>
            <p>Update (rename) a database</p>
            <h4>Example request:</h4>
            <code>
curl -X PUT \
  http://your-api-base-url.com/api/databases \
  -H 'Code: 040800' \
  -H 'Content-Type: application/json' \
  -d '{"name": "old_database_name", "new_name": "new_database_name"}'
            </code>
            <h4>Example response:</h4>
            <code>
{"message": "Database renamed successfully"}
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">DELETE</span> <span class="url">/api/databases</span></h3>
            <p>Delete a database</p>
            <h4>Example request:</h4>
            <code>
curl -X DELETE \
  http://your-api-base-url.com/api/databases \
  -H 'Code: 040800' \
  -H 'Content-Type: application/json' \
  -d '{"name": "database_to_delete"}'
            </code>
            <h4>Example response:</h4>
            <code>
{"message": "Database deleted successfully"}
            </code>
        </div>
    </details>

    <details>
        <summary>CRUD Operations</summary>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/api/crud/{table}</span></h3>
            <p>Get all records from a table</p>
            <h4>Example request:</h4>
            <code>
curl -X GET \
  http://your-api-base-url.com/api/crud/users \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db'
            </code>
            <h4>Example response:</h4>
            <code>
[
  {"id": 1, "name": "John Doe", "email": "john@example.com"},
  {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/api/crud/{table}</span></h3>
            <p>Create a new record</p>
            <h4>Example request:</h4>
            <code>
curl -X POST \
  http://your-api-base-url.com/api/crud/users \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Alice Johnson", "email": "alice@example.com"}'
            </code>
            <h4>Example response:</h4>
            <code>
{"id": 3}
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">PUT</span> <span class="url">/api/crud/{table}/{id}</span></h3>
            <p>Update a specific record</p>
            <h4>Example request:</h4>
            <code>
curl -X PUT \
  http://your-api-base-url.com/api/crud/users/3 \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Alice Johnson Updated", "email": "alice.updated@example.com"}'
            </code>
            <h4>Example response:</h4>
            <code>
{"updated": 1}
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">DELETE</span> <span class="url">/api/crud/{table}/{id}</span></h3>
            <p>Delete a specific record</p>
            <h4>Example request:</h4>
            <code>
curl -X DELETE \
  http://your-api-base-url.com/api/crud/users/3 \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db'
            </code>
            <h4>Example response:</h4>
            <code>
{"deleted": 1}
            </code>
        </div>
    </details>

    <details>
        <summary>Database Import/Export</summary>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/api/import</span></h3>
            <p>Import a database file</p>
            <h4>Example request:</h4>
            <code>
curl -X POST \
  http://your-api-base-url.com/api/import \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db' \
  -H 'Content-Type: application/json' \
  -d '{"file": "base64_encoded_file_data"}'
            </code>
            <h4>Example response:</h4>
            <code>
{"message": "Database imported successfully"}
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/api/export</span></h3>
            <p>Export a database file</p>
            <h4>Example request:</h4>
            <code>
curl -X GET \
  http://your-api-base-url.com/api/export \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db' \
  --output mydatabase.db
            </code>
            <p>This will download the database file.</p>
        </div>
    </details>

    <details>
        <summary>Media Operations</summary>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/api/media</span></h3>
            <p>List all media files</p>
            <h4>Example request:</h4>
            <code>
curl -X GET \
  http://your-api-base-url.com/api/media \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db'
            </code>
            <h4>Example response:</h4>
            <code>
["image1.jpg", "document.pdf", "video.mp4"]
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/api/media/{filename}</span></h3>
            <p>Upload a media file</p>
            <h4>Example request:</h4>
            <code>
curl -X POST \
  http://your-api-base-url.com/api/media/newimage.jpg \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db' \
  -H 'Content-Type: image/jpeg' \
  --data-binary '@/path/to/local/image.jpg'
            </code>
            <h4>Example response:</h4>
            <code>
{"message": "File uploaded successfully"}
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/api/media/{filename}</span></h3>
            <p>Download a media file</p>
            <h4>Example request:</h4>
            <code>
curl -X GET \
  http://your-api-base-url.com/api/media/image1.jpg \
  -H 'Database: mydatabase.db' \
  --output image1.jpg
            </code>
            <p>This will download the media file.</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">DELETE</span> <span class="url">/api/media/{filename}</span></h3>
            <p>Delete a media file</p>
            <h4>Example request:</h4>
            <code>
curl -X DELETE \
  http://your-api-base-url.com/api/media/image1.jpg \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db'
            </code>
            <h4>Example response:</h4>
            <code>
{"message": "File deleted successfully"}
            </code>
        </div>
    </details>

    <details>
        <summary>Query Execution</summary>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/api/query</span></h3>
            <p>Execute a SELECT query</p>
            <h4>Example request:</h4>
            <code>
curl -X POST \
  http://your-api-base-url.com/api/query \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db' \
  -H 'Content-Type: application/json' \
  -d '{"query": "SELECT * FROM users WHERE age > 18"}'
            </code>
            <h4>Example response:</h4>
            <code>
[
  {"id": 1, "name": "John Doe", "age": 30},
  {"id": 2, "name": "Jane Smith", "age": 25}
]
            </code>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/api/execute</span></h3>
            <p>Execute a non-SELECT query</p>
            <h4>Example request:</h4>
            <code>
curl -X POST \
  http://your-api-base-url.com/api/execute \
  -H 'Code: 040800' \
  -H 'Database: mydatabase.db' \
  -H 'Content-Type: application/json' \
  -d '{"query": "UPDATE users SET status = 'active' WHERE last_login > '2023-01-01'"}'
            </code>
            <h4>Example response:</h4>
            <code>
{"affected_rows": 5}
            </code>
        </div>
    </details>

</body>
</html>
        """