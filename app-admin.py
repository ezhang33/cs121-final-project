"""
Student name(s): Edward Zhang
Student email(s): ezhang3@caltech.edu
High-level program overview

******************************************************************************
Store Simulation for cars that are on sale. It should be able to help users 
efficiently browse through thousands to hundreds of thousands cars on sale, 
and help them filter based on their specific desires such as make, model, 
year, and price. It will also provide a lot of helpful information when 
looking at purchasing a car, such as the fuel type, transmission type 
(automatic or manual), number of previous owners, mileage, and more.

******************************************************************************
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
import hashlib

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='appadmin',
            password='adminpw',
            port='3306',  # this may change!
            database='cardealershipdb'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)
def authenticate_user(connection, username, password):
    """Authenticate a user by checking the username and password."""
    query = """
    SELECT username, salt, password_hash FROM user_info WHERE username = %s
    """
    cursor = connection.cursor()
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    if user:
        salt = user[1]
        password_hash = hashlib.sha256((salt + password).encode()).hexdigest()
        if password_hash == user[2]:
            return True
    return False

def get_user_role(connection, username):
    """Get the role of the user: either buyer, seller, or admin."""
    query = """
    SELECT role FROM user_info WHERE username = %s
    """
    cursor = connection.cursor()
    cursor.execute(query, (username,))
    role = cursor.fetchone()
    if role:
        return role[0]
    return None

def user_login(connection):
    """Handles user login."""
    username = input("Enter username: ")
    password = input("Enter password: ")

    if authenticate_user(connection, username, password):
        print("Login successful!")
        role = get_user_role(connection, username)
        if role:
            print(f"Logged in as {role}.")
            return role
        else:
            print("Role not found. Please contact the administrator.")
            return None
    else:
        print("Invalid username or password.")
        return None

# ----------------------------------------------------------------------
# Admin-Specific Functions
# ----------------------------------------------------------------------

def show_admin_options():
    """
    Displays options specific to admin users, like managing users, cars, etc.
    """
    print('What would you like to do as an admin?')
    print('  (v) - view all users')
    print('  (m) - manage users (add/update/delete)')
    print('  (q) - quit')
    ans = input('Enter an option: ').lower()

    if ans == 'v':
        view_all_users()
    elif ans == 'm':
        manage_users()
    elif ans == 'q':
        quit_ui()


def view_all_users():
    """View all users in the system."""
    query = """
    SELECT username, role FROM user_info
    """
    cursor = conn.cursor()
    cursor.execute(query)
    users = cursor.fetchall()

    if users:
        for user in users:
            print(f"Username: {user[0]} | Role: {user[1]}")
    else:
        print("No users found.")


def manage_users():
    """Manage users (add, update, or delete)."""
    action = input("Do you want to (a)dd, (u)pdate, or (d)elete a user? ").lower()

    if action == 'a':
        add_user()
    elif action == 'u':
        update_user()
    elif action == 'd':
        delete_user()


def add_user():
    """Add a new user."""
    username = input("Enter new username: ")
    role = input("Enter user role (buyer/seller/admin): ").lower()
    password = input("Enter password: ")
    salt = "some_salt"
    password_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    query = """
    INSERT INTO user_info (username, password_hash, salt, role)
    VALUES (%s, %s, %s, %s)
    """
    cursor = conn.cursor()
    cursor.execute(query, (username, password_hash, salt, role))
    conn.commit()
    print("User added successfully.")


def update_user():
    """Update user information (like role)."""
    username = input("Enter username to update: ")
    new_role = input("Enter new role (buyer/seller/admin): ").lower()

    query = """
    UPDATE user_info SET role = %s WHERE username = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (new_role, username))
    conn.commit()
    print(f"User {username} updated successfully.")


def delete_user():
    """Delete a user."""
    username = input("Enter username to delete: ")

    query = """
    DELETE FROM user_info WHERE username = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (username,))
    conn.commit()
    print(f"User {username} deleted successfully.")

def view_all_cars():
    """Admin can view all cars in the system."""
    query = """
    SELECT car_id, car_make, car_model, car_year, car_color, price FROM car
    """
    cursor = conn.cursor()
    cursor.execute(query)
    cars = cursor.fetchall()

    if cars:
        for car in cars:
            print(f"Car ID: {car[0]} | {car[1]} {car[2]} ({car[3]}) - ${car[5]} | Color: {car[4]}")
    else:
        print("No cars found.")

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_admin_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
