-- 4-init.sql
-- Initial setup for items and orders tables

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS items (
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 10,
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS orders (
    item_name VARCHAR(255) NOT NULL,
    number INT NOT NULL,
    FOREIGN KEY (item_name) REFERENCES items(name)
);

INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");

