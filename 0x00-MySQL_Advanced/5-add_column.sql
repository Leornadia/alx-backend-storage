-- 5-add_column.sql
ALTER TABLE users
ADD COLUMN valid_email BOOLEAN NOT NULL DEFAULT 0;

