-- CS 121
-- Final Project
-- Setup file for defining and loading Car Dealership information

-- Drop database if exists and recreate a new one
DROP DATABASE IF EXISTS cardealershipdb;
CREATE DATABASE cardealershipdb;
USE cardealershipdb;

-- Clean up old tables, dropping tables with foreign keys first
DROP TABLE IF EXISTS costs;
DROP TABLE IF EXISTS found_at;
DROP TABLE IF EXISTS offering;
DROP TABLE IF EXISTS getting;
DROP TABLE IF EXISTS listed;
DROP TABLE IF EXISTS bought;
DROP TABLE IF EXISTS cost;
DROP TABLE IF EXISTS dealer;
DROP TABLE IF EXISTS car;
DROP TABLE IF EXISTS listing;
DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS seller;
DROP TABLE IF EXISTS buyer;
DROP TABLE IF EXISTS user;

-- CREATE TABLE commands:
-- User of the car store simulator
-- Either a buyer, a seller, or both
CREATE TABLE user (
    user_id     VARCHAR(10),
    -- Type of user, e.g. ('buyer', 'seller', or 'both')
    user_type   VARCHAR(10)   NOT NULL,
    PRIMARY KEY (user_id)
);

-- User information for logging in and authentication
CREATE TABLE user_info (
    user_id             VARCHAR(10),
    username            VARCHAR(50)      NOT NULL UNIQUE,
    password_hash       VARCHAR(64)      NOT NULL,
    salt                VARCHAR(32)      NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE
);

-- Buyer who finds cars and buys them
CREATE TABLE buyer (
    user_id              VARCHAR(10),
    user_type            VARCHAR(10)        NOT NULL 
        CHECK(user_type = 'buyer' OR user_type = 'both'),
    first_name           VARCHAR(15)        NOT NULL,
    last_name            VARCHAR(15)        NOT NULL,
    email                VARCHAR(30)        NOT NULL UNIQUE,
    phone_number         VARCHAR(30)        NOT NULL UNIQUE,
    credit_card          VARCHAR(16)        UNIQUE,
    exp_date             DATE,
    verification_code    VARCHAR(3),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE
);

-- The purchased transaction made by a buyer
CREATE TABLE purchase (
    purchase_id     VARCHAR(10),
    purchase_time   TIMESTAMP   NOT NULL,
    confirmation    VARCHAR(6)  NOT NULL UNIQUE,
    PRIMARY KEY (purchase_id)
);

-- Seller from a dealership who lists cars for sale
CREATE TABLE seller (
    user_id                 VARCHAR(10),
    user_type               VARCHAR(10)        NOT NULL 
        CHECK(user_type = 'seller' OR user_type = 'both'),
    first_name              VARCHAR(15) NOT NULL,
    last_name               VARCHAR(15) NOT NULL,
    email                   VARCHAR(30) NOT NULL UNIQUE,
    phone_number            VARCHAR(30)        NOT NULL UNIQUE,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE
);

-- The listing made by a seller
CREATE TABLE listing (
    listing_id     VARCHAR(10),
    listing_time   TIMESTAMP    NOT NULL,
    confirmation    VARCHAR(6)  NOT NULL UNIQUE,
    PRIMARY KEY (listing_id)
);

-- Represents cars for sale, uniquely identified by car_id
CREATE TABLE car (
    car_id          INT            AUTO_INCREMENT,
    car_make        VARCHAR(100)   NOT NULL,
    car_model       VARCHAR(100)   NOT NULL,
    car_year        YEAR           NOT NULL,
    car_color       VARCHAR(50),
    mileage         INT,
    number_owners   INT,
    transmission    VARCHAR(25)    NOT NULL,
    fuel            VARCHAR(25)    NOT NULL,
    PRIMARY KEY (car_id)
);

CREATE TABLE dealer (
    dealer_id       INT            AUTO_INCREMENT,
    dealership      VARCHAR(250)   NOT NULL,
    dealer_location VARCHAR(250)   NOT NULL,
    PRIMARY KEY (dealer_id)
);

-- Cost for the car
CREATE TABLE cost (
    car_id          INT,
    price           NUMERIC(8, 2)  NOT NULL,
    msrp            NUMERIC(8, 2)  NOT NULL,
    PRIMARY KEY (car_id),
    FOREIGN KEY (car_id) REFERENCES car(car_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Relationship-set between a buyer and a purchase
CREATE TABLE bought (
    purchase_id    VARCHAR(10),
    user_id        VARCHAR(10),
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (purchase_id) REFERENCES purchase(purchase_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE
);

-- Relationship-set between a seller and a listing
CREATE TABLE listed (
    listing_id     VARCHAR(10),
    user_id        VARCHAR(10),
    PRIMARY KEY (listing_id),
    FOREIGN KEY (listing_id) REFERENCES listing(listing_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE
);

-- Relationship-set between a purchase and a car
CREATE TABLE getting (
    car_id        INT,
    purchase_id   VARCHAR(10),
    PRIMARY KEY (car_id),
    FOREIGN KEY (car_id) REFERENCES car(car_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (purchase_id) REFERENCES purchase(purchase_id) 
        ON DELETE CASCADE
);

-- Relationship-set between a listing and a car
CREATE TABLE offering (
    car_id        INT,
    listing_id    VARCHAR(10),
    PRIMARY KEY (car_id),
    FOREIGN KEY (car_id) REFERENCES car(car_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (listing_id) REFERENCES listing(listing_id) 
        ON DELETE CASCADE
);

-- Relationship-set between dealer and car
CREATE TABLE found_at (
    car_id        INT,
    dealer_id     INT,
    date_added    TIMESTAMP,
    PRIMARY KEY (car_id),
    FOREIGN KEY (car_id) REFERENCES car(car_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (dealer_id) REFERENCES dealer(dealer_id) 
        ON DELETE CASCADE
);

-- Relationship-set between car and cost
CREATE TABLE costs (
    car_id           INT,
    price            NUMERIC(8, 2),
    PRIMARY KEY (car_id, price),
    FOREIGN KEY (car_id) REFERENCES cost(car_id) ON DELETE CASCADE
);

-- Index for searching by car_make and car_model
CREATE INDEX idx_car_make_model ON car(car_make, car_model);

-- Create a View for Car Details with Seller, Buyer, and Pricing Info
CREATE VIEW car_overview AS
SELECT c.car_id, c.car_make, c.car_model, c.car_year, c.car_color, 
       c.mileage, c.number_owners, c.transmission, c.fuel,
       s.first_name AS seller_first_name, s.last_name AS seller_last_name, 
       s.email AS seller_email, s.phone_number AS seller_phone,
       b.first_name AS buyer_first_name, b.last_name AS buyer_last_name, 
       b.email AS buyer_email, b.phone_number AS buyer_phone,
       co.price AS current_price, co.msrp AS suggested_price
FROM car AS c
LEFT JOIN offering AS o ON c.car_id = o.car_id
LEFT JOIN listing AS l ON o.listing_id = l.listing_id
LEFT JOIN listed AS li ON l.listing_id = li.listing_id
LEFT JOIN seller AS s ON li.user_id = s.user_id
LEFT JOIN getting AS g ON c.car_id = g.car_id
LEFT JOIN purchase AS p ON g.purchase_id = p.purchase_id
LEFT JOIN bought AS bo ON p.purchase_id = bo.purchase_id
LEFT JOIN buyer AS b ON bo.user_id = b.user_id
LEFT JOIN cost AS co ON c.car_id = co.car_id;
