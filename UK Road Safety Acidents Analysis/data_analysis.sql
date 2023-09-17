-- Create "day_of_week" table
CREATE TABLE day_of_week(
id INTEGER PRIMARY KEY,
day_name VARCHAR(20) NOT NULL);

-- Create "accident" table
CREATE TABLE accident (
accident_index VARCHAR(13) PRIMARY KEY,
location_easting_osgr NUMERIC,
location_northing_osgr NUMERIC,
longitude  NUMERIC,
latitude NUMERIC,
police_force INTEGER,
accident_severity INTEGER,
number_of_vehicle INTEGER,
number_of_casualties INTEGER,
date DATE,
day_of_week_id INTEGER REFERENCES day_of_week(id),
time TIME);

-- Create "vehicle_type" table
CREATE TABLE vehicle_type (
id INTEGER PRIMARY KEY,
label TEXT UNIQUE);

-- Create "vehicle" table
CREATE TABLE vehicle (
id SERIAL PRIMARY KEY,
accident_index VARCHAR,
vehicle_type_id INTEGER REFERENCES vehicle_type(id),
age_of_driver INTEGER,
engine_capacity_cc INTEGER,
propulsion_code INTEGER);

-- Insert data into day_of_week table
INSERT INTO day_of_week(id,day_name) VALUES
(1,'Sunday'),
(2,'Monday'),
(3,'Tuesday'),
(4,'Wednesday'),
(5,'Thursday'),
(6,'Friday'),
(7,'Saturday');

-- Load data into the tables using \copy command
\copy accident FROM '/Users/ORESANYA/Classic Isaac/Git/PostgreSQL/dataset/accident_preprocessed.csv' WITH (FORMAT CSV, HEADER);
\copy vehicle_type(id,model) FROM '/Users/ORESANYA/Classic Isaac/Git/PostgreSQL/dataset/vehicle_type.csv' WITH (FORMAT CSV, HEADER);
\copy vehicle(accident_index,vehicle_type_id,age_of_driver,engine_capacity_cc,propulsion_code) FROM '/Users/ORESANYA/Classic Isaac/Git/PostgreSQL/dataset/vehicle_preprocessed.csv' WITH (FORMAT CSV, HEADER);

--Select and display the first 5 rows from the accident table
SELECT * FROM accident LIMIT 5;
--Select and display the first 5 rows from the vehicle table
SELECT * FROM vehicle LIMIT 5;
-- Select and display all rows from the vehicle_type table
SELECT * FROM vehicle_type;

-- Count the number of accidents in the dataset
SELECT COUNT(*) FROM accident;

-- Create index on acident_index column
CREATE INDEX idx_accident_index ON accident(accident_index);

-- Create index on the accident_index colun and the vehicle_type_id column which are both frequently used in queries
CREATE INDEX idx_vehicle_acident_type ON vehicle(accident_index,vehicle_type_id);
-- Count the number of accidents by severity level and order them by count
SELECT accident_severity,COUNT(accident_severity)
FROM accident GROUP BY accident_severity
ORDER BY COUNT(accident_severity) DESC;

-- Count the number of accident by day of the week and order them by day of the week
SELECT day_of_week.day_name,COUNT(accident.day_of_week_id)
FROM day_of_week
JOIN accident ON day_of_week.id=accident.day_of_week_id
GROUP BY day_of_week.day_name,accident.day_of_week_id
ORDER BY accident.day_of_week_id;

-- Find the most common vehicle types involved in accidents and order them by count
SELECT vehicle_type.label,COUNT(vehicle.vehicle_type_id)
FROM vehicle_type
FULL JOIN vehicle ON vehicle_type.id=vehicle.vehicle_type_id
GROUP BY vehicle_type.label
ORDER BY COUNT(vehicle.vehicle_type_id) DESC;

-- Find the average age of drivers involved in accidents
SELECT AVG(age_of_driver) FROM vehicle;

-- Count the number of accidents that occured in each month of the year and order them by month
SELECT EXTRACT(month FROM date) AS month,COUNT(date)
FROM accident GROUP BY month
ORDER BY month;

-- Count the number of accidents by hour of day and police force, and order them by police force
SELECT police_force,EXTRACT(hour FROM time) AS hour,count(*) AS num_accidents
FROM accident GROUP BY police_force,hour
ORDER BY police_force,hour;

-- Select data from accident, day_of_week, vehicle, and vehicle_type tables
-- join the tables based on the specified foreign key relationships
SELECT accident.date,day_of_week.day_name,accident.accident_severity,
vehicle_type.label,vehicle.age_of_driver
FROM accident
FULL JOIN vehicle ON accident.accident_index=vehicle.accident_index
JOIN vehicle_type ON vehicle.vehicle_type_id=vehicle_type.id
JOIN day_of_week ON accident.day_of_week_id=day_of_week.id;

