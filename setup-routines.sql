-- UDF Function to calculate the discounted price of a car.
-- Takes in the original price and the discount percentage as parameters.
-- Best for sellers who want to update one of their listings and put a 
-- discount on it, and want to quickly calculate their new discounted price
DELIMITER $$

CREATE FUNCTION calculate_discounted_price(original_price DECIMAL(10, 2), 
                                           discount_percentage DECIMAL(5, 2))
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE discounted_price DECIMAL(10, 2);
    SET discounted_price = original_price - 
        (original_price * discount_percentage / 100);
    RETURN discounted_price;
END $$

DELIMITER ;

-- Procedure to update the price of a specific car based on car_id
-- Helpful for sellers who have calculated a good discount price
-- and now want to actually update the cost of their listed car
DELIMITER $$

CREATE PROCEDURE sp_update_car_price(car_id INT, new_price DECIMAL(10, 2))
BEGIN
    UPDATE cost
    SET price = new_price
    WHERE car_id = car_id;
END $$

DELIMITER ;
