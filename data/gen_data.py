import csv
import random
from faker import Faker

fake = Faker()

# Define realistic car makes and models
car_makes_and_models = {
    "Toyota": ["Corolla", "Camry", "Prius", "Highlander", "Tacoma"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey"],
    "Ford": ["Mustang", "Focus", "F-150", "Explorer", "Escape"],
    "Chevrolet": ["Malibu", "Silverado", "Equinox", "Traverse", "Impala"],
    "BMW": ["3 Series", "5 Series", "X5", "X3", "M3"],
    "Nissan": ["Altima", "Sentra", "Maxima", "Rogue", "Murano"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Kona"],
    "Kia": ["Optima", "Sorento", "Sportage", "Forte", "Telluride"],
    "Volkswagen": ["Jetta", "Golf", "Passat", "Tiguan", "Atlas"],
    "Audi": ["A4", "A6", "Q5", "Q7", "A3"]
}

# Function to generate random data for users
def generate_user_data(num):
    users = []
    for _ in range(num):
        user_type = random.choice(['buyer', 'seller', 'both'])
        user_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
        users.append([user_id, user_type])
    return users

# Function to generate buyer data
def generate_buyer_data(num, users):
    buyers = []
    for i in range(num):
        user_id = users[i][0]
        buyer_data = [user_id, 'buyer' if users[i][1] == 'buyer' else 'both', 
                      fake.first_name(), fake.last_name(), 
                      fake.email(), format_phone_number(''.join(random.choices('0123456789', k=10))), generate_credit_card_number(), 
                      fake.date(), fake.credit_card_security_code()]
        buyers.append(buyer_data)
    return buyers

# Function to generate a 16-digit credit card number
def generate_credit_card_number():
    return ''.join(random.choices('0123456789', k=16))

# Function to format phone number as (xxx) xxx-xxxx
def format_phone_number(phone):
    return f"({phone[0:3]}) {phone[3:6]}-{phone[6:11]}"

# Function to generate purchase data
def generate_purchase_data(num, buyers):
    purchases = []
    for i in range(num):
        purchase_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))  # VARCHAR(10) format
        purchase_time = fake.date_time_this_decade()
        confirmation = fake.unique.bothify(text="??????")
        purchases.append([purchase_id, purchase_time, confirmation])
    return purchases

# Function to generate seller data
def generate_seller_data(num, users):
    sellers = []
    for i in range(num):
        user_id = users[i][0]
        seller_data = [user_id, 'seller' if users[i][1] == 'seller' else 'both', 
                       fake.first_name(), fake.last_name(), 
                       fake.email(), format_phone_number(''.join(random.choices('0123456789', k=10)))]
        sellers.append(seller_data)
    return sellers

# Function to generate listing data
def generate_listing_data(num):
    listings = []
    for i in range(num):
        listing_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))  # VARCHAR(10) format
        listing_time = fake.date_time_this_decade()
        confirmation = fake.unique.bothify(text="??????")
        listings.append([listing_id, listing_time, confirmation])
    return listings

# Function to generate car data
def generate_car_data(num):
    cars = []
    for i in range(num):
        car_make = random.choice(list(car_makes_and_models.keys()))  # Choose a random car make
        car_model = random.choice(car_makes_and_models[car_make])  # Choose a model from the selected make
        car_year = random.randint(1990, 2023)
        car_color = random.choice([fake.color_name(), None])  # Random color, could be None
        mileage = random.randint(5000, 200000) if random.choice([True, False]) else None
        number_owners = random.randint(1, 5) if random.choice([True, False]) else None
        transmission = random.choice(['automatic', 'manual'])
        fuel = random.choice(['petrol', 'diesel', 'electric'])
        cars.append([i+1, car_make, car_model, car_year, car_color, mileage, number_owners, transmission, fuel])
    return cars

# List of US cities and states (realistic cities and states for dealership locations)
us_cities_and_states = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"),
    ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"),
    ("Dallas", "TX"), ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("San Francisco", "CA"),
    ("Indianapolis", "IN"), ("Seattle", "WA"), ("Denver", "CO"), ("Washington", "DC"),
    ("Boston", "MA"), ("El Paso", "TX"), ("Nashville", "TN"), ("Detroit", "MI"),
    ("Oklahoma City", "OK"), ("Portland", "OR"), ("Las Vegas", "NV"), ("Memphis", "TN"),
    ("Louisville", "KY"), ("Baltimore", "MD"), ("Milwaukee", "WI"), ("Albuquerque", "NM"),
    ("Tucson", "AZ"), ("Fresno", "CA"), ("Sacramento", "CA"), ("Kansas City", "MO"),
    ("Long Beach", "CA"), ("Mesa", "AZ"), ("Atlanta", "GA"), ("Colorado Springs", "CO"),
    ("Raleigh", "NC"), ("Miami", "FL"), ("Omaha", "NE"), ("Oakland", "CA"),
    ("Minneapolis", "MN"), ("Tulsa", "OK"), ("Arlington", "TX"), ("New Orleans", "LA"),
    ("Wichita", "KS"), ("Cleveland", "OH"), ("Tampa", "FL"), ("Bakersfield", "CA"),
    ("Aurora", "CO"), ("Anaheim", "CA"), ("Honolulu", "HI"), ("Santa Ana", "CA"),
    ("Riverside", "CA"), ("Corpus Christi", "TX"), ("Lexington", "KY"), ("St. Louis", "MO"),
    ("Stockton", "CA"), ("Pittsburgh", "PA"), ("St. Paul", "MN"), ("Cincinnati", "OH"),
    ("Anchorage", "AK"), ("Henderson", "NV"), ("Greensboro", "NC"), ("Plano", "TX"),
    ("Newark", "NJ"), ("Lincoln", "NE"), ("Toledo", "OH"), ("Chula Vista", "CA"),
    ("Buffalo", "NY"), ("Fort Wayne", "IN"), ("Jersey City", "NJ"), ("Chandler", "AZ"),
    ("Madison", "WI"), ("Lubbock", "TX"), ("Scottsdale", "AZ"), ("Reno", "NV")
]

# Function to generate random dealer data with realistic locations
def generate_dealer_data(num):
    dealers = []
    for i in range(num):
        dealership = fake.company()
        city, state = random.choice(us_cities_and_states)  # Random city and state
        dealer_location = f"{city}, {state}"
        dealers.append([i+1, dealership, dealer_location])
    return dealers

# Function to generate cost data
def generate_cost_data(num, cars):
    cost = []
    costs = []
    for i in range(num):
        car_id = cars[i][0]
        price = round(random.uniform(1000, 50000), 2)
        msrp = round(random.uniform(1000, 50000), 2)
        cost.append([car_id, price, msrp])
        costs.append([car_id, price])
    return cost, costs

# Function to generate bought data
def generate_bought_data(num, purchases, buyers):
    bought = []
    for i in range(num):
        purchase_id = purchases[i][0]
        user_id = buyers[i % len(buyers)][0]
        bought.append([purchase_id, user_id])
    return bought

# Function to generate getting data
def generate_getting_data(num, cars, purchases):
    getting = []
    for i in range(num):
        car_id = cars[i % len(cars)][0]
        purchase_id = purchases[i % len(purchases)][0]
        getting.append([car_id, purchase_id])
    return getting

# Function to generate listed data
def generate_listed_data(num, sellers, listings):
    listed = []
    for i in range(num):
        listing_id = listings[i][0]
        user_id = sellers[i % len(sellers)][0]
        listed.append([listing_id, user_id])
    return listed

# Function to generate offering data
def generate_offering_data(num, cars, listings):
    offering = []
    for i in range(num):
        car_id = cars[i % len(cars)][0]
        listing_id = listings[i % len(listings)][0]
        offering.append([car_id, listing_id])
    return offering

# Function to generate found_at data (cars assigned to dealers)
def generate_found_at_data(num, cars, dealers):
    found_at = []
    for i in range(num):
        car_id = cars[i % len(cars)][0]
        dealer_id = random.choice(dealers)[0]  # Randomly assign a car to one of the 10 dealers
        date_added = fake.date_this_decade()
        found_at.append([car_id, dealer_id, date_added])
    return found_at

# Write to CSV
def write_to_csv(filename, data, headers):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Data generation
users = generate_user_data(100)
buyers = generate_buyer_data(100, users)
purchases = generate_purchase_data(50, buyers)
sellers = generate_seller_data(100, users)
listings = generate_listing_data(100)
cars = generate_car_data(100)
dealers = generate_dealer_data(10)  # Only 10 dealers
cost, costs = generate_cost_data(100, cars)
bought = generate_bought_data(50, purchases, buyers)
getting = generate_getting_data(50, cars, purchases)
listed = generate_listed_data(100, sellers, listings)
offering = generate_offering_data(100, cars, listings)
found_at = generate_found_at_data(100, cars, dealers)  # Assign cars to dealers

# Write to CSV files
write_to_csv('user.csv', users, ['user_id', 'user_type'])
write_to_csv('buyer.csv', buyers, ['user_id', 'user_type', 'first_name', 'last_name', 'email', 'phone_number', 'credit_card', 'exp_date', 'verification_code'])
write_to_csv('purchase.csv', purchases, ['purchase_id', 'purchase_time', 'confirmation'])
write_to_csv('seller.csv', sellers, ['user_id', 'user_type', 'first_name', 'last_name', 'email', 'phone_number'])
write_to_csv('listing.csv', listings, ['listing_id', 'listing_time', 'confirmation'])
write_to_csv('car.csv', cars, ['car_id', 'car_make', 'car_model', 'car_year', 'car_color', 'mileage', 'number_owners', 'transmission', 'fuel'])
write_to_csv('dealer.csv', dealers, ['dealer_id', 'dealership', 'dealer_location'])
write_to_csv('cost.csv', cost, ['car_id', 'price', 'msrp'])
write_to_csv('costs.csv', costs, ['car_id', 'price'])
write_to_csv('bought.csv', bought, ['purchase_id', 'user_id'])
write_to_csv('getting.csv', getting, ['car_id', 'purchase_id'])
write_to_csv('listed.csv', listed, ['listing_id', 'user_id'])
write_to_csv('offering.csv', offering, ['car_id', 'listing_id'])
write_to_csv('found_at.csv', found_at, ['car_id', 'dealer_id', 'date_added'])
