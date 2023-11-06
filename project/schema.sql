DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS record;

CREATE TABLE record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    time TEXT NOT NULL,
    second INTEGER NOT NULL,
    result TEXT NOT NULL,
    date TEXT NOT NULL
);