-- name: create_table
CREATE TABLE test (
       id INT PRIMARY KEY AUTO_INCREMENT,
       a TEXT NOT NULL,
       b INT NOT NULL
)

-- name: clean_test!
-- Make sure we have a clean test table
TRUNCATE TABLE test

-- name: insert_test
-- Example of how to insert a new value and use parameters
INSERT INTO test (a, b) VALUES (%(a)s, %(b)s)

-- name: all_test
-- This is what a result looks like
SELECT * FROM test
