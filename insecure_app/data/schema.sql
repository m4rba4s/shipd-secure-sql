DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS articles;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL
);

INSERT INTO users (username, password, role) VALUES
    ('admin', 'supersecret', 'administrator'),
    ('jane', 'pass123', 'editor'),
    ('mike', 'qwerty', 'reader');

INSERT INTO articles (title, body) VALUES
    ('Understanding Flask', 'A quick primer on building web apps with Flask.'),
    ('Intro to SQL', 'Learn how SQL queries are structured and executed.'),
    ('Security Basics', 'Why input validation and parameterised queries matter.');
