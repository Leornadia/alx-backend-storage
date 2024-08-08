-- Import the table dump (run this in the terminal, not inside the SQL script)
-- mysql -uroot -p holberton < names.sql

-- Create the index on the first letter of the 'name' column
CREATE INDEX idx_name_first ON names (name(1));

-- Verify the index creation
SHOW INDEX FROM names;

-- Example query to test the performance
SELECT COUNT(name) FROM names WHERE name LIKE 'a%';

