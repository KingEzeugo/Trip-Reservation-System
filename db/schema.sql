DROP TABLE IF EXISTS reservations;

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    row INTEGER NOT NULL,
    col INTEGER NOT NULL,
    cost REAL NOT NULL,
    code TEXT NOT NULL UNIQUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS admins;

CREATE TABLE admins (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
