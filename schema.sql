CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator_id INTEGER REFERENCES users,
    visible BOOLEAN
);

CREATE TABLE categories_tunes (
    category_id INTEGER REFERENCES categories, 
    tune_id INTEGER REFERENCES tunes,
    PRIMARY KEY (category_id, tune_id)
);

CREATE TABLE tunes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    notation TEXT,
    created TIMESTAMP WITHOUT TIME ZONE,
    creator_id INTEGER REFERENCES users,
    visible BOOLEAN
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
);