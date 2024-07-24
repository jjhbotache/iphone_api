# Simple API Project on an Old iPhone 4

This project is a simple API running on an old iPhone 4. The API is built with Python 2.5 and provides basic CRUD operations for databases, media services, and SQL query endpoints. Below, you'll find detailed documentation for using the API.

## Project Overview

This project demonstrates the capability to run a web server and handle API requests on outdated hardware. It utilizes SQLite as the database engine and serves media files from dedicated folders.

## API Documentation

### Authentication

All requests (except GET requests to media files) require a `Code` header with the value `040800`. Requests without this header will receive a "Permission denied" error.

### Database Operations

- **GET /api/databases** - List all databases
  - Retrieve a list of all databases in the system.
  - **Headers:** `Code: 040800`
  - **Response:**
    ```json
    ["database1.db", "database2.db"]
    ```

- **POST /api/databases** - Create a new database
  - Create a new SQLite database.
  - **Headers:** `Code: 040800`, `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "name": "new_database"
    }
    ```
  - **Response:**
    ```json
    {
        "message": "Database created successfully"
    }
    ```

### CRUD Operations

All CRUD operations require a `Database` header specifying which database to use.

- **GET /api/crud/{table}** - List all records
  - Retrieve all records from the specified table.
  - **Headers:** `Code: 040800`, `Database: database_name.db`
  - **Example:** `GET /api/crud/users`
  - **Response:**
    ```json
    [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    ]
    ```

- **GET /api/crud/{table}/{id}** - Get a specific record
  - Retrieve a specific record by ID from the specified table.
  - **Headers:** `Code: 040800`, `Database: database_name.db`
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
  - **Headers:** `Code: 040800`, `Database: database_name.db`, `Content-Type: application/json`
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
  - **Headers:** `Code: 040800`, `Database: database_name.db`, `Content-Type: application/json`
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
  - **Headers:** `Code: 040800`, `Database: database_name.db`
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
  - **Headers:** `Code: 040800`, `Database: database_name.db`, `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "file": "base64_encoded_database_content"
    }
    ```
  - **Response:**
    ```json
    {
        "message": "Database imported successfully"
    }
    ```

- **GET /api/export** - Export the current database
  - Export the current database as a downloadable file.
  - **Headers:** `Code: 040800`, `Database: database_name.db`
  - **Response:** The database file will be downloaded.

### Media Service

Media files are stored in folders named `<database_name>_MEDIA`.

- **GET /api/media** - List files in the media directory
  - Retrieve a list of all files in the media directory for the specified database.
  - **Headers:** `Code: 040800`, `Database: database_name.db`
  - **Response:**
    ```json
    [
        "file1.jpg",
        "file2.png"
    ]
    ```

- **GET /api/media/{filename}** - Get a specific file
  - Retrieve a specific file from the media directory by its filename.
  - **Headers:** `Database: database_name.db`
  - **Response:** The file will be downloaded.

- **POST /api/media/{filename}** - Upload a file
  - Upload a new file to the media directory. The file content must be base64 encoded.
  - **Headers:** `Code: 040800`, `Database: database_name.db`, `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "file": "base64_encoded_file_content"
    }
    ```
  - **Response:**
    ```json
    {
        "message": "File uploaded successfully"
    }
    ```

- **DELETE /api/media/{filename}** - Delete a file
  - Delete a specific file from the media directory by its filename.
  - **Headers:** `Code: 040800`, `Database: database_name.db`
  - **Response:**
    ```json
    {
        "message": "File deleted successfully"
    }
    ```

### SQL Query Endpoints

- **POST /api/query** - Execute a SELECT query
  - Execute a SELECT SQL query on the specified database.
  - **Headers:** `Code: 040800`, `Database: database_name.db`, `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "query": "SELECT * FROM users WHERE age > 18"
    }
    ```
  - **Response:**
    ```json
    [
        {"id": 1, "name": "John Doe", "age": 30},
        {"id": 2, "name": "Jane Smith", "age": 25}
    ]
    ```
  - **Note:** This endpoint only allows SELECT queries for security reasons.

- **POST /api/execute** - Execute a modifying query
  - Execute an SQL query that modifies the specified database (INSERT, UPDATE, DELETE).
  - **Headers:** `Code: 040800`, `Database: database_name.db`, `Content-Type: application/json`
  - **Body:**
    ```json
    {
        "query": "INSERT INTO users (name, age) VALUES ('John Doe', 30)"
    }
    ```
  - **Response:**
    ```json
    {
        "affected_rows": 1
    }
    ```
  - **Note:** This endpoint does not allow SELECT queries. Use `/api/query` for SELECT operations.

### Error Handling

All API endpoints return JSON responses, including error messages. Example error response:

```json
{
    "error": "Database not found"
}
```

### Running the Server

To run the server, execute the `main.py` script:

```
python main.py
```

The server will start on port 8000 by default.