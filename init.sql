--sample db for testing the api
-- init.sql

-- Create a users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into the users table
INSERT INTO users (username, email) VALUES
    ('john_doe', 'john@example.com'),
    ('jane_smith', 'jane@example.com');

-- Create a products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Insert sample data into the products table
INSERT INTO products (name,price) VALUES
    ('Laptop', 999.99),
    ('Smartphone', 499.99),
    ('Headphones', 79.99);
