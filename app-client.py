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
            user='appclient',
            password='clientpw',
            port='3306',  # this may change!
            database='cardealershipdb'
        )
        print('Successfully connected.')
        return conn
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr.write('Incorrect username or password when connecting to DB.\n')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr.write('Database does not exist.\n')
        elif DEBUG:
            sys.stderr.write(f"Error: {err}\n")
        else:
            sys.stderr.write('An error occurred, please contact the administrator.\n')
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
    """Get the role of the user: either buyer or seller."""
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
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_buyer_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do as a buyer?')
    print('  (s) - search for cars')
    print('  (f) - filter search results')
    print('  (v) - view car details')
    print('  (b) - buy car')
    print('  (q) - quit')
    ans = input('Enter an option: ').lower()
    if ans == 's':
        search_cars()
    elif ans == 'f':
        filter_cars()
    elif ans == 'v':
        view_car_details()
    elif ans == 'b':
        buy_car()
    elif ans == 'q':
        quit_ui()


def show_seller_options():
    """
    Displays options specific for sellers, such as adding a listing,
    updating a listing, or deleting a listing.
    """
    print('What would you like to do as a seller?')
    print('  (a) - add a new listing')
    print('  (e) - edit a current listing')
    print('  (d) - delete a current listing')
    print('  (q) - quit')
    ans = input('Enter an option: ').lower()

    if ans == 'a':
        add_listing()
    elif ans == 'e':
        edit_listing()
    elif ans == 'd':
        delete_listing()
    elif ans == 'q':
        quit_ui()


def search_cars():
    """Allow buyers to search for cars."""
    make = input("Enter car make (e.g., Toyota): ")
    max_price = float(input("Enter maximum price: "))
    query = """
    SELECT car_id, car_make, car_model, car_year, car_color, price
    FROM car
    WHERE car_make = %s AND price < %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (make, max_price))
    cars = cursor.fetchall()

    if cars:
        for car in cars:
            print(f"Car ID: {car[0]} | {car[1]} {car[2]} ({car[3]}) - ${car[5]} | Color: {car[4]}")
    else:
        print("No cars found.")

def filter_cars():
    """Allow buyers to filter cars."""
    print("Implement filter functionality here based on specific criteria.")

def view_car_details():
    """Allow buyers to view car details."""
    car_id = input("Enter car ID to view details: ")
    query = """
    SELECT * FROM car WHERE car_id = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (car_id,))
    car = cursor.fetchone()
    
    if car:
        print(f"Car ID: {car[0]} | Make: {car[1]} | Model: {car[2]} | Year: {car[3]} | Color: {car[4]}")
        # Additional car details like mileage, transmission, fuel type, etc.
    else:
        print("Car not found.")

def buy_car():
    """Allow buyers to buy a car."""
    car_id = input("Enter car ID to buy: ")
    query = """
    UPDATE car SET status = 'sold' WHERE car_id = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (car_id,))
    conn.commit()
    print(f"Car with ID {car_id} purchased successfully.")

def add_listing():
    """Allow sellers to add a new car listing."""
    car_make = input("Enter car make: ")
    car_model = input("Enter car model: ")
    car_year = int(input("Enter car year: "))
    car_color = input("Enter car color: ")
    price = float(input("Enter price: "))

    query = """
    INSERT INTO car (car_make, car_model, car_year, car_color, price)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor = conn.cursor()
    cursor.execute(query, (car_make, car_model, car_year, car_color, price))
    conn.commit()
    print("Car listing added successfully.")

def edit_listing():
    """Allow sellers to edit an existing car listing."""
    car_id = input("Enter car ID to edit: ")
    new_price = float(input("Enter new price: "))

    query = """
    UPDATE car SET price = %s WHERE car_id = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (new_price, car_id))
    conn.commit()
    print(f"Car with ID {car_id} updated successfully.")

def delete_listing():
    """Allow sellers to delete a car listing."""
    car_id = input("Enter car ID to delete: ")
    query = """
    DELETE FROM car WHERE car_id = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (car_id,))
    conn.commit()
    print(f"Car with ID {car_id} deleted successfully.")

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
    role = user_login(conn)
    if not role:
        print("Login failed. Exiting program.")
        sys.exit(1)

    if role == 'buyer':
        while True:
            show_buyer_options()
    elif role == 'seller':
        while True:
            show_seller_options()

if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
