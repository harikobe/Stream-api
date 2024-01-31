# Stream Data API

This project is a FastAPI-based web application designed to handle streaming data. It includes Docker configurations for setting up a PostgreSQL database, pgAdmin for database management, and the FastAPI application.

## Getting Started

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/harikobe/Stream-api.git
    ```

2. **Create a `.env` File:**

    Create a `.env` file in the root directory and set the required environment variables:

    ```env
    DB_USER=your_postgres_user
    DB_PASSWORD=your_postgres_password
    DB_HOST=postgres_container_name
    DB_PORT=your_postgres_container_port
    PGADMIN_EMAIL=your_pgadmin_email
    PGADMIN_PASSWORD=your_pgadmin_password
    ```

3. **`init.sql` - SQL File for Tables:**

    The `init.sql` file is provided for creating your own tables. During the Docker Compose, the tables are created in the default PostgreSQL database in pgAdmin. This file is for testing purposes.

4. **Build and Start Docker Containers:**

    ```bash
    docker-compose up -d
    ```

5. **Access the Applications:**

    - Access the FastAPI application at [http://localhost:8000](http://localhost:8000).
    - Access pgAdmin at [http://localhost:5050](http://localhost:5050).

## How It Works

1. After composing the Docker Compose file, check pgAdmin [http://localhost:5050] and the FastAPI app [http://localhost:8000].

2. Access the FastAPI Swagger-UI for visual API documentation.

3. Enter the database name that you created, and the response will be in JSON format, displaying tables, columns, and data in the response body.
