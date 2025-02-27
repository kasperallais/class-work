SET search_path TO kallais, berkeley_meters;

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
	SELECT * FROM meters
	WHERE (label ILIKE '%main%' AND label ILIKE '%demand%')
	AND units='kW'
);
CALL check_view('q1', ARRAY['id', 'label', 'site', 'units'], 23);

CREATE VIEW q2 AS (
	SELECT 
		id,
		label,
		regexp_replace(
			regexp_replace(
				regexp_replace(site, '\(.*\)', ''), ' NEW ', ''), ' New ', '') AS clean_site, 
		units 
	FROM q1
);
CALL check_view('q2', ARRAY['id', 'label', 'clean_site', 'units'], 23);

CREATE VIEW q3 AS (
    SELECT DISTINCT clean_site FROM q2
);
CALL check_view('q3', ARRAY[ 'clean_site'], 14);

CREATE VIEW q4 AS (
	SELECT q2.clean_site, COUNT(DISTINCT q2.id) as num_meters, COUNT(data.id) AS num_data_points
	FROM q2
	LEFT JOIN data on q2.id = data.id
	GROUP BY q2.clean_site
	HAVING COUNT(data.id) > 0
);
CALL check_view('q4', ARRAY['clean_site', 'num_meters', 'num_data_points'], 13);

CREATE VIEW q5 AS (
	SELECT clean_site FROM q3 EXCEPT SELECT clean_site FROM q4
);
CALL check_view('q5', ARRAY['clean_site'], 1);

CREATE VIEW q6 AS (
	SELECT time_diff, id, site
	FROM (
		SELECT 
		(d.time - LAG(d.time) OVER (PARTITION BY d.id ORDER BY d.time)) AS time_diff,
		d.id,
		q2.clean_site AS site
		FROM data AS d
		JOIN q2 ON d.id = q2.id
	) AS sub 
	WHERE time_diff > INTERVAL '16 minutes'	
);
CALL check_view('q6', ARRAY['time_diff', 'id', 'site'], 1);

CREATE VIEW q7 AS (
	SELECT q2.clean_site AS site,
	d.time,
	SUM(d.value) AS value
	FROM data AS d
	JOIN q2 ON d.id = q2.id
	WHERE q2.clean_site NOT IN (
		SELECT DISTINCT site FROM q6
	)
	GROUP BY q2.clean_site, d.time
);
CALL check_view('q7', ARRAY['site', 'time', 'value'], 7737);

CREATE VIEW q8 AS (
	WITH site_counts AS (
		SELECT site,
      COUNT(*) FILTER (WHERE value <> 0) AS nonzero_count
    FROM q7
    GROUP BY site
  ),
  stats AS (
    SELECT 
      AVG(nonzero_count) AS avg_count, 
      STDDEV(nonzero_count) AS std_count
    FROM site_counts
  )
  SELECT site
  FROM site_counts, stats
  WHERE nonzero_count < (avg_count - std_count)
     OR nonzero_count > (avg_count + std_count)
);
CALL check_view('q8', ARRAY['site'], 5);

--- put q9 answer in README.txt

CREATE VIEW q10 AS (
	SELECT q7.site, (SUM(q7.value) / 4.0) / r.net_sqft AS weekly_eui
	FROM q7
	JOIN real_estate AS r
	ON q7.site = r.building_name
	WHERE q7.site NOT IN (SELECT site FROM q8)
	GROUP BY q7.site, r.net_sqft
);
CALL check_view('q10', ARRAY['site', 'weekly_eui'], 7);

CREATE VIEW q11 AS (
	SELECT
	regr_slope(q10.weekly_eui, (2023 - r.year)) AS slope,
	regr_intercept(q10.weekly_eui, (2023 - r.year)) AS intercept,
	corr(q10.weekly_eui, (2023 - r.year)) AS corr
	FROM q10
	JOIN real_estate AS r ON q10.site = r.building_name
);
CALL check_view('q11', ARRAY['slope', 'intercept', 'corr'], 1);

--- put q12 answer in README.txt
