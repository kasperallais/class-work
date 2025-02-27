SET search_path TO YOUR_USERNAME, berkeley_meters;

DROP VIEW IF EXISTS q11;
DROP VIEW IF EXISTS q10;
DROP VIEW IF EXISTS q8;
DROP VIEW IF EXISTS q7;
DROP VIEW IF EXISTS q6;
DROP VIEW IF EXISTS q5;
DROP VIEW IF EXISTS q4;
DROP VIEW IF EXISTS q3;
DROP VIEW IF EXISTS q2;
DROP VIEW IF EXISTS q1;

CREATE VIEW q1 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q1', ARRAY['id', 'label', 'site', 'units'], 23);

CREATE VIEW q2 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q2', ARRAY['id', 'label', 'clean_site', 'units'], 23);

CREATE VIEW q3 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q3', ARRAY[ 'clean_site'], 14);

CREATE VIEW q4 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q4', ARRAY['clean_site', 'num_meters', 'num_data_points'], 13);

CREATE VIEW q5 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q5', ARRAY['clean_site'], 1);

CREATE VIEW q6 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q6', ARRAY['time_diff', 'id', 'site'], 1);

CREATE VIEW q7 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q7', ARRAY['site', 'time', 'value'], 7737);

CREATE VIEW q8 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q8', ARRAY['site'], 5);

--- put q9 answer in README.txt

CREATE VIEW q10 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q10', ARRAY['site', 'weekly_eui'], 7);

CREATE VIEW q11 AS (
    SELECT 'YOUR CODE HERE'
);
CALL check_view('q11', ARRAY['slope', 'intercept', 'corr'], 1);

--- put q12 answer in README.txt
