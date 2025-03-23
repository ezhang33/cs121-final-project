-- Some sample queries for our car dealership database

-- Search for all cars sold at a certain dealership ordered by price
-- Best for buyers who want to go to a dealership close to where they live
-- and are looking for just about any car on a budget
-- Search for all cars sold at a certain dealership ordered by price
SELECT c.car_id, c.car_make, c.car_model, c.car_year, c.car_color, co.price
FROM car AS c
JOIN found_at AS fa ON c.car_id = fa.car_id
JOIN dealer AS d ON fa.dealer_id = d.dealer_id
JOIN cost AS co ON c.car_id = co.car_id
WHERE d.dealer_id = 1
ORDER BY co.price ASC;

-- Computes the average price of cars sold by each dealer
SELECT d.dealer_id, d.dealer_location, AVG(co.price) AS avg_price
FROM dealer AS d
JOIN found_at AS fa ON d.dealer_id = fa.dealer_id
JOIN car AS c ON fa.car_id = c.car_id
JOIN cost AS co ON c.car_id = co.car_id
GROUP BY d.dealer_id, d.dealer_location
ORDER BY avg_price DESC;

-- Finds all Toyota cars below a certain price along with the dealer they are at
SELECT c.car_id, c.car_make, c.car_model, c.car_year, c.car_color, co.price, 
       d.dealership AS dealer_name, 
       d.dealer_location
FROM car AS c
JOIN cost AS co ON c.car_id = co.car_id
JOIN found_at AS fa ON c.car_id = fa.car_id
JOIN dealer AS d ON fa.dealer_id = d.dealer_id
WHERE c.car_make = 'Toyota' 
    AND co.price < 25000
ORDER BY co.price ASC;

-- Updates the price of a specific car
UPDATE cost 
SET price = price - 1000 
WHERE car_id = 5;
