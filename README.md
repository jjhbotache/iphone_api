# Simple API Project on an Old iPhone 4

This project is a simple API running on an old iPhone 4. The API is built with Python 2.5 and provides basic CRUD operations, media services, and SQL query endpoints. Below, you'll find detailed documentation for using the API.

## Project Overview

This project demonstrates the capability to run a web server and handle API requests on outdated hardware. It utilizes SQLite as the database and serves media files from a dedicated folder.

## API Documentation

### CRUD Operations

- **GET /api/crud/{table}** - List all records
  - Retrieve all records from the specified table.
  - **Headers:** None
  - **Example:** `GET /api/crud/users`
  - **Response:**
    ```json
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    ```

- **GET /api/crud/{table}/{id}** - Get a specific record
  - Retrieve a specific record by ID from the specified table.
  - **Headers:** None
  - **Example:** `GET /api/crud/users/1`
  - **Response:**
    ```json
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    ```

- **POST /api/crud/{table}** - Create a new record
  - Create a new record in the specified table.
  - **Headers:** `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    ```
  - **Example:** `POST /api/crud/users`
  - **Response:**
    ```json
    {
        "id": 1
    }
    ```

- **PUT /api/crud/{table}/{id}** - Update an existing record
  - Update a specific record by ID in the specified table.
  - **Headers:** `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "name": "John Smith",
        "email": "john.smith@example.com"
    }
    ```
  - **Example:** `PUT /api/crud/users/1`
  - **Response:**
    ```json
    {
        "updated": 1
    }
    ```

- **DELETE /api/crud/{table}/{id}** - Delete a record
  - Delete a specific record by ID from the specified table.
  - **Headers:** None
  - **Example:** `DELETE /api/crud/users/1`
  - **Response:**
    ```json
    {
        "deleted": 1
    }
    ```

### Database Import/Export

- **POST /api/import** - Import a database
  - Import a new database. The database file must be base64 encoded.
  - **Headers:** `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "file": "base64_encoded_database_content"
    }
    ```
  - **Example:** `POST /api/import`
  - **Response:**
    ```json
    {
        "message": "Database imported successfully"
    }
    ```

- **GET /api/export** - Export the current database
  - Export the current database as a downloadable file.
  - **Headers:** None
  - **Example:** `GET /api/export`
  - **Response:** The database file will be downloaded.

### Media Service

- **GET /api/media** - List files in the media directory
  - Retrieve a list of all files in the media directory.
  - **Headers:** None
  - **Example:** `GET /api/media`
  - **Response:**
    ```json
    [
        "file1.jpg",
        "file2.png"
    ]
    ```

- **GET /api/media/{filename}** - Get a specific file
  - Retrieve a specific file from the media directory by its filename.
  - **Headers:** None
  - **Example:** `GET /api/media/file1.jpg`
  - **Response:** The file will be downloaded.

- **POST /api/media/{filename}** - Upload a file
  - Upload a new file to the media directory. The file content must be base64 encoded.
  - **Headers:** `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "file": "base64_encoded_file_content"
    }
    ```
  - **Example:** `POST /api/media/file1.jpg`
  - **Response:**
    ```json
    {
        "message": "File uploaded successfully"
    }
    ```

- **DELETE /api/media/{filename}** - Delete a file
  - Delete a specific file from the media directory by its filename.
  - **Headers:** None
  - **Example:** `DELETE /api/media/file1.jpg`
  - **Response:**
    ```json
    {
        "message": "File deleted successfully"
    }
    ```

### SQL Query Endpoints

- **POST /api/query** - Execute a SELECT query
  - Execute a SELECT SQL query on the database.
  - **Headers:** `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "query": "SELECT * FROM users WHERE age > 18"
    }
    ```
  - **Example:** `POST /api/query`
  - **Response:**
    ```json
    {
        "results": [
            {"id": 1, "name": "John Doe", "age": 30},
            {"id": 2, "name": "Jane Smith", "age": 25}
        ]
    }
    ```
  - **Note:** This endpoint only allows SELECT queries for security reasons.

- **POST /api/execute** - Execute a modifying query
  - Execute an SQL query that modifies the database (INSERT, UPDATE, DELETE).
  - **Headers:** `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "query": "INSERT INTO users (name, age) VALUES ('John Doe', 30)"
    }
    ```
  - **Example:** `POST /api/execute`
  - **Response:**
    ```json
    {
        "message": "Query executed successfully",
        "affected_rows": 1
    }
    ```
  - **Note:** This endpoint does not allow SELECT queries. Use `/api/query` for SELECT operations.

### Request and Response Format

- All requests and responses are in JSON format.
- **Headers:**
  - `Content-Type: application/json` - Required for POST and PUT requests to specify that the request body contains JSON data.

### Example Requests

#### GET Request
```http
GET /api/crud/users HTTP/1.1
Host: localhost:8000
