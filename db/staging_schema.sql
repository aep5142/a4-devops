-- Create staging database
CREATE DATABASE IF NOT EXISTS staging_db;

-- Use staging database
USE staging_db;

-- Create todo table
CREATE TABLE IF NOT EXISTS todo_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    todo VARCHAR(255) NOT NULL
);

-- Insert some test to-do items
INSERT INTO todo_table (todo) VALUES ('Run 10k');
INSERT INTO todo_table (todo) VALUES ('Devops HW');
INSERT INTO todo_table (todo) VALUES ('Cloud HW');