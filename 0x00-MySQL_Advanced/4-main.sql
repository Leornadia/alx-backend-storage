-- 4-main.sql
-- Show and add orders to test the trigger

-- Show initial state of the tables
SELECT * FROM items;
SELECT * FROM orders;

-- Insert orders to trigger the update on items
INSERT INTO orders (item_name, number) VALUES ('apple', 1);
INSERT INTO orders (item_name, number) VALUES ('apple', 3);
INSERT INTO orders (item_name, number) VALUES ('pear', 2);

-- Show updated state of the tables
SELECT "--";
SELECT * FROM items;
SELECT * FROM orders;

