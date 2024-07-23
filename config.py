# -*- coding: utf-8 -*-

DB_NAME = 'database.db'
MEDIA_FOLDER = 'media'
DOCUMENTATION_HTML = """
        <html>
<head>
    <title>API Documentation</title>
</head>
<body>
    <h1>API Documentation</h1>

    <h2>CRUD Operations</h2>
    <ul>
        <li>
            <strong>GET /api/crud/{table}</strong> - List all records
            <p>Retrieve all records from the specified table.</p>
            <p><strong>Headers:</strong> None</p>
            <p><strong>Example:</strong> GET /api/crud/users</p>
            <p><strong>Response:</strong>
                <pre>
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
}
                </pre>
            </p>
        </li>
        <li>
            <strong>GET /api/crud/{table}/{id}</strong> - Get a specific record
            <p>Retrieve a specific record by ID from the specified table.</p>
            <p><strong>Headers:</strong> None</p>
            <p><strong>Example:</strong> GET /api/crud/users/1</p>
            <p><strong>Response:</strong>
                <pre>
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
}
                </pre>
            </p>
        </li>
        <li>
            <strong>POST /api/crud/{table}</strong> - Create a new record
            <p>Create a new record in the specified table.</p>
            <p><strong>Headers:</strong> Content-Type: application/json</p>
            <p><strong>Body:</strong>
                <pre>
{
    "name": "John Doe",
    "email": "john.doe@example.com"
}
                </pre>
            </p>
            <p><strong>Example:</strong> POST /api/crud/users</p>
            <p><strong>Response:</strong>
                <pre>
{
    "id": 1
}
                </pre>
            </p>
        </li>
        <li>
            <strong>PUT /api/crud/{table}/{id}</strong> - Update an existing record
            <p>Update a specific record by ID in the specified table.</p>
            <p><strong>Headers:</strong> Content-Type: application/json</p>
            <p><strong>Body:</strong>
                <pre>
{
    "name": "John Smith",
    "email": "john.smith@example.com"
}
                </pre>
            </p>
            <p><strong>Example:</strong> PUT /api/crud/users/1</p>
            <p><strong>Response:</strong>
                <pre>
{
    "updated": 1
}
                </pre>
            </p>
        </li>
        <li>
            <strong>DELETE /api/crud/{table}/{id}</strong> - Delete a record
            <p>Delete a specific record by ID from the specified table.</p>
            <p><strong>Headers:</strong> None</p>
            <p><strong>Example:</strong> DELETE /api/crud/users/1</p>
            <p><strong>Response:</strong>
                <pre>
{
    "deleted": 1
}
                </pre>
            </p>
        </li>
    </ul>

    <h2>Database Import/Export</h2>
    <ul>
        <li>
            <strong>POST /api/import</strong> - Import a database
            <p>Import a new database. The database file must be base64 encoded.</p>
            <p><strong>Headers:</strong> Content-Type: application/json</p>
            <p><strong>Body:</strong>
                <pre>
{
    "file": "base64_encoded_database_content"
}
                </pre>
            </p>
            <p><strong>Example:</strong> POST /api/import</p>
            <p><strong>Response:</strong>
                <pre>
{
    "message": "Database imported successfully"
}
                </pre>
            </p>
        </li>
        <li>
            <strong>GET /api/export</strong> - Export the current database
            <p>Export the current database as a downloadable file.</p>
            <p><strong>Headers:</strong> None</p>
            <p><strong>Example:</strong> GET /api/export</p>
            <p><strong>Response:</strong> The database file will be downloaded.</p>
        </li>
    </ul>

    <h2>Media Service</h2>
    <ul>
        <li>
            <strong>GET /api/media</strong> - List files in the media directory
            <p>Retrieve a list of all files in the media directory.</p>
            <p><strong>Headers:</strong> None</p>
            <p><strong>Example:</strong> GET /api/media</p>
            <p><strong>Response:</strong>
                <pre>
[
    "file1.jpg",
    "file2.png"
]
                </pre>
            </p>
        </li>
        <li>
            <strong>GET /api/media/{filename}</strong> - Get a specific file
            <p>Retrieve a specific file from the media directory by its filename.</p>
            <p><strong>Headers:</strong> None</p>
            <p><strong>Example:</strong> GET /api/media/file1.jpg</p>
            <p><strong>Response:</strong> The file will be downloaded.</p>
        </li>
        <li>
            <strong>POST /api/media/{filename}</strong> - Upload a file
            <p>Upload a new file to the media directory. The file content must be base64 encoded.</p>
            <p><strong>Headers:</strong> Content-Type: application/json</p>
            <p><strong>Body:</strong>
                <pre>
{
    "file": "base64_encoded_file_content"
}
                </pre>
            </p>
            <p><strong>Example:</strong> POST /api/media/file1.jpg</p>
            <p><strong>Response:</strong>
                <pre>
{
    "message": "File uploaded successfully"
}
                </pre>
            </p>
        </li>
        <li>
            <strong>DELETE /api/media/{filename}</strong> - Delete a file
            <p>Delete a specific file from the media directory by its filename.</p>
            <p><strong>Headers:</strong> None</p>
            <p><strong>Example:</strong> DELETE /api/media/file1.jpg</p>
            <p><strong>Response:</strong>
                <pre>
{
    "message": "File deleted successfully"
}
                </pre>
            </p>
        </li>
    </ul>

    <h2>SQL Query Endpoints</h2>
    <ul>
        <li>
            <strong>POST /api/query</strong> - Execute a SELECT query
            <p>Execute a SELECT SQL query on the database.</p>
            <p><strong>Headers:</strong> Content-Type: application/json</p>
            <p><strong>Body:</strong>
                <pre>
{
    "query": "SELECT * FROM users WHERE age > 18"
}
                </pre>
            </p>
            <p><strong>Example:</strong> POST /api/query</p>
            <p><strong>Response:</strong>
                <pre>
{
    "results": [
        {"id": 1, "name": "John Doe", "age": 30},
        {"id": 2, "name": "Jane Smith", "age": 25}
    ]
}
                </pre>
            </p>
            <p><strong>Note:</strong> This endpoint only allows SELECT queries for security reasons.</p>
        </li>
        <li>
            <strong>POST /api/execute</strong> - Execute a modifying query
            <p>Execute an SQL query that modifies the database (INSERT, UPDATE, DELETE).</p>
            <p><strong>Headers:</strong> Content-Type: application/json</p>
            <p><strong>Body:</strong>
                <pre>
{
    "query": "INSERT INTO users (name, age) VALUES ('John Doe', 30)"
}
                </pre>
            </p>
            <p><strong>Example:</strong> POST /api/execute</p>
            <p><strong>Response:</strong>
                <pre>
{
    "message": "Query executed successfully",
    "affected_rows": 1
}
                </pre>
            </p>
            <p><strong>Note:</strong> This endpoint does not allow SELECT queries. Use /api/query for SELECT operations.</p>
        </li>
    </ul>

    <h2>Request and Response Format</h2>
    <p>All requests and responses are in JSON format. The following headers are used for different types of requests:</p>
    <ul>
        <li><strong>Content-Type: application/json</strong> - This header is required for POST and PUT requests to specify that the request body contains JSON data.</li>
    </ul>

    <h2>Example Requests</h2>
    <h3>GET Request</h3>
    <pre>
GET /api/crud/users HTTP/1.1
Host: localhost:8000
    </pre>

    <h3>POST Request</h3>
    <pre>
POST /api/crud/users HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
}
    </pre>

    <h3>PUT Request</h3>
    <pre>
PUT /api/crud/users/1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
}
    </pre>

    <h3>DELETE Request</h3>
    <pre>
DELETE /api/crud/users/1 HTTP/1.1
Host: localhost:8000
    </pre>

    <h3>SQL Query Request</h3>
    <pre>
POST /api/query HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "query": "SELECT * FROM users WHERE age > 18"
}
    </pre>

    <h3>SQL Execute Request</h3>
    <pre>
POST /api/execute HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "query": "INSERT INTO users (name, age) VALUES ('John Doe', 30)"
}
    </pre>

    <h2>Handling Responses</h2>
    <p>All responses from the API will be in JSON format. The response will include relevant data based on the request made. In case of an error, an appropriate HTTP status code and error message will be returned.</p>

    <h2>Error Codes</h2>
    <ul>
        <li><strong>200 OK</strong> - The request was successful.</li>
        <li><strong>201 Created</strong> - A new resource was successfully created (for POST requests).</li>
        <li><strong>400 Bad Request</strong> - The request was invalid or cannot be served.</li>
        <li><strong>404 Not Found</strong> - The requested resource could not be found.</li>
        <li><strong>500 Internal Server Error</strong> - An error occurred on the server.</li>
    </ul>

    <h2>Security Considerations</h2>
    <p>When using the SQL query endpoints, please keep the following security considerations in mind:</p>
    <ul>
        <li>The /api/query endpoint only allows SELECT queries to prevent unintended modifications to the database.</li>
        <li>The /api/execute endpoint is designed for INSERT, UPDATE, and DELETE operations. It does not allow SELECT queries.</li>
        <li>Always sanitize and validate user input before using it in SQL queries to prevent SQL injection attacks.</li>
        <li>Consider implementing additional authentication and authorization measures to control access to these endpoints.</li>
        <li>Monitor and log the usage of these endpoints to detect any potential misuse or security issues.</li>
    </ul>
</body>
</html>

        """