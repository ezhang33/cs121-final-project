-- Permissions for both clients and admins
DROP USER IF EXISTS 'appadmin'@'localhost';
DROP USER IF EXISTS 'appclient'@'localhost';

CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'clientpw';

-- Grant all privileges to the appadmin user for the car dealership database
GRANT ALL PRIVILEGES ON cardealershipdb.* TO 'appadmin'@'localhost';

-- Grant SELECT privileges to the appclient user (buyers can only read)
GRANT SELECT ON cardealershipdb.* TO 'appclient'@'localhost';

-- Grant INSERT privileges to the appclient user if they are sellers
GRANT INSERT ON cardealershipdb.car TO 'appclient'@'localhost';
GRANT INSERT ON cardealershipdb.dealer TO 'appclient'@'localhost';
GRANT INSERT ON cardealershipdb.cost TO 'appclient'@'localhost';
-- Also grant UPDATE priveleges to sellers
GRANT UPDATE ON cardealershipdb.car TO 'appclient'@'localhost';
GRANT UPDATE ON cardealershipdb.dealer TO 'appclient'@'localhost';
GRANT UPDATE ON cardealershipdb.cost TO 'appclient'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
