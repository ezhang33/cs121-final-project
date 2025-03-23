-- Loads data from the csv files into our sql database
-- Load data into user table
LOAD DATA LOCAL INFILE 'data/user.csv' 
INTO TABLE user 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into buyer table
LOAD DATA LOCAL INFILE 'data/buyer.csv' 
INTO TABLE buyer 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into purchase table
LOAD DATA LOCAL INFILE 'data/purchase.csv' 
INTO TABLE purchase 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into seller table
LOAD DATA LOCAL INFILE 'data/seller.csv' 
INTO TABLE seller 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into listing table
LOAD DATA LOCAL INFILE 'data/listing.csv' 
INTO TABLE listing 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into car table
LOAD DATA LOCAL INFILE 'data/car.csv' 
INTO TABLE car 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into dealer table
LOAD DATA LOCAL INFILE 'data/dealer.csv' 
INTO TABLE dealer 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into cost table
LOAD DATA LOCAL INFILE 'data/cost.csv' 
INTO TABLE cost 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into costs table
LOAD DATA LOCAL INFILE 'data/costs.csv' 
INTO TABLE costs 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into bought table
LOAD DATA LOCAL INFILE 'data/bought.csv' 
INTO TABLE bought 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into getting table
LOAD DATA LOCAL INFILE 'data/getting.csv' 
INTO TABLE getting 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into listed table
LOAD DATA LOCAL INFILE 'data/listed.csv' 
INTO TABLE listed 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into offering table
LOAD DATA LOCAL INFILE 'data/offering.csv' 
INTO TABLE offering 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- Load data into found_at table
LOAD DATA LOCAL INFILE 'data/found_at.csv' 
INTO TABLE found_at 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;
