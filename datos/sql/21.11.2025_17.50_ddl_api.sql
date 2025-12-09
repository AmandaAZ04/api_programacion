CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    website VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL,

    CONSTRAINT fk_todos_users FOREIGN KEY (userId)
    REFERENCES users(id)
);