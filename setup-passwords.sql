-- CS 121 24wi: Password Management (A6 and Final Project)

-- (Provided) This function generates a specified number of characters for 
-- using as a salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

-- Provided (you may modify in your FP if you choose)
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you
-- have admin or other roles for users in your application
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- User type ('buyer', 'seller', 'both')
    user_type VARCHAR(10) NOT NULL,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL
);

-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20),
                 new_user_type VARCHAR(10))
BEGIN
    DECLARE new_salt CHAR(8);
    DECLARE salted_password BINARY(64);

    SET new_salt = make_salt(8);
    SET salted_password = SHA2(CONCAT(new_salt, password), 256);

    INSERT INTO user_info (username, user_type, salt, password_hash)
    VALUES (new_username, new_user_type, new_salt, salted_password);
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE current_salt CHAR(8);
    DECLARE current_hash BINARY(64);
    DECLARE computed_hash BINARY(64);

    SELECT salt, password_hash
    INTO current_salt, current_hash
    FROM user_info
    WHERE user_info.username = username;

    IF current_salt IS NULL THEN
        RETURN 0;
    END IF;

    SET computed_hash = SHA2(CONCAT(current_salt, password), 256);

    IF computed_hash = current_hash THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END !
DELIMITER ;

-- Create a procedure sp_change_password to generate a new salt and change 
-- the given user's password to the given password (after salting and hashing)
DELIMITER !
CREATE PROCEDURE sp_change_password(username VARCHAR(20), 
                 new_password VARCHAR(20))
BEGIN
    DECLARE new_salt CHAR(8);
    DECLARE new_password_hash BINARY(64);

    SET new_salt = make_salt(8);
    SET new_password_hash = SHA2(CONCAT(new_salt, new_password), 256);

    UPDATE user_info
    SET salt = new_salt, password_hash = new_password_hash
    WHERE user_info.username = username;
END !
DELIMITER ;