import datetime
import sqlite3
import re

# create a connection to the database
conn = sqlite3.connect('db.sqlite')

# create a cursor object to execute SQL statements
cur = conn.cursor()


# function to verify email
def get_email_input(prompt):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while True:
        email = input(prompt).strip()
        if not email:
            print("Please enter a non-empty email address.")
            continue
        elif not re.match(email_regex, email):
            print("Please enter a valid email address.")
            continue
        else:
            return email


# function to verify user input
def get_input(prompt, validator):
    while True:
        value = input(prompt)
        try:
            validator(value)
            return value
        except ValueError as e:
            print(e)


# validate name format
def validate_name(name_str):
    if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', name_str):
        raise ValueError("Invalid name format. Please enter a name with only letters and spaces.")


# validate datetime format
def validate_datetime(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect datetime format. Please use the format 'YYYY-MM-DD HH:MM:SS'.")


# validate float format
def validate_float(float_str):
    try:
        float(float_str)
    except ValueError:
        raise ValueError("Invalid float format.")


# validate integer format
def validate_non_negative_int(int_str):
    try:
        int_value = int(int_str)
        if int_value < 0:
            raise ValueError("Invalid integer format. Please enter a non-negative integer.")
    except ValueError:
        raise ValueError("Invalid integer format.")


# validate latitude and longitude format
def validate_lat_or_long(lat_or_long_str):
    # regular expression pattern for latitude or longitude
    lat_or_long_regex = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$'
    if not re.match(lat_or_long_regex, lat_or_long_str):
        raise ValueError("Invalid latitude/longitude format.")


# validate maintenance type
def validate_maintenance_type(maintenance_type):
    if maintenance_type not in ('repair', 'charge', 'move'):
        raise ValueError("Invalid asset type. Please enter 'repair', 'charge', or 'move'.")


# validate asset type
def validate_asset_type(asset_type):
    if asset_type not in ('bike', 'scooter'):
        raise ValueError("Invalid asset type. Please enter 'bike' or 'scooter'.")


# validate payment method
def validate_payment_method(rider_payment_method):
    if rider_payment_method not in ('debit_card', 'credit_card', 'bank_transfer', 'paypal'):
        raise ValueError("Invalid payment method. Please enter 'debit_card', 'credit_card', 'bank_transfer', or 'paypal'.")


# validate zone type
def validate_arrival_zone_type(zone_type):
    if zone_type not in ('parking', 'slow', 'disabled'):
        raise ValueError("Invalid asset type. Please enter 'parking', 'slow', or 'disabled'.")


# get user input to add data to the Assets table
print("Add records to Assets table:")
asset_type = get_input("Enter the asset type (bike/scooter): ", validate_asset_type)
asset_model = input("Enter the asset model: ")
cur.execute("INSERT INTO Assets (asset_type, asset_model) VALUES (?, ?)", (asset_type, asset_model))
print("Data added to Assets table.\n")

# get user input to add data to the Riders table
print("Add records to Riders table:")
rider_email = get_email_input("Enter the rider email: ")
rider_name = get_input("Enter the rider name: ", validate_name)
rider_password = input("Enter the rider password: ")
rider_payment_method = get_input("Enter the rider payment method: ", validate_payment_method)
cur.execute("INSERT INTO Riders (rider_email, rider_name, rider_password, rider_payment_method) VALUES (?, ?, ?, ?)",
            (rider_email, rider_name, rider_password, rider_payment_method))
print("Data added to Riders table.\n")

# get user input to add data to the Pricing table
print("Add records to Pricing table:")
asset_model = input("Enter the asset model: ")
unlock_price = get_input("Enter the unlock price: ", validate_float)
minute_price = get_input("Enter the minute price: ", validate_float)
kilometer_price = get_input("Enter the kilometer price: ", validate_float)
cur.execute("INSERT INTO Pricing (asset_model, unlock_price, minute_price, kilometer_price) VALUES (?, ?, ?, ?)",
            (asset_model, unlock_price, minute_price, kilometer_price))
print("Data added to Pricing table.\n")

# get user input to add data to the Maintenance_Activity table
print("Add records to Maintenance_Activity table:")
asset_id = get_input("Enter the asset id: ", validate_non_negative_int)
maintenance_start_time = get_input("Enter the maintenance start time (YYYY-MM-DD HH:MM:SS): ", validate_datetime)
maintenance_end_time = get_input("Enter the maintenance end time (YYYY-MM-DD HH:MM:SS): ", validate_datetime)
maintenance_technician = get_input("Enter the maintenance technician: ", validate_name)
maintenance_type = get_input("Enter the maintenance type (repair/charge/move): ", validate_maintenance_type)
maintenance_notes = input("Enter the maintenance notes: ")
cur.execute(
    "INSERT INTO MaintenanceActivity (asset_id, maintenance_start_time, maintenance_end_time, maintenance_technician, maintenance_type, maintenance_notes) VALUES (?, ?, ?, ?, ?, ?)",
    (asset_id, maintenance_start_time, maintenance_end_time, maintenance_technician, maintenance_type,
     maintenance_notes))
print("Data added to Maintenance_Activity table.\n")

# get user input to add data to the Zones table
print("Add records to Zones table:")
zone_jurisdiction = input("Enter the zone jurisdiction: ")
zone_type = get_input("Enter the zone type (parking/slow/disabled): ", validate_arrival_zone_type)
cur.execute("INSERT INTO Zones (zone_jurisdiction, zone_type) VALUES (?, ?)", (zone_jurisdiction, zone_type))
print("Data added to Zones table.\n")

# get user input to add data to the Journeys table
print("Add records to Journeys table:")
rider_email = get_email_input("Enter the rider email: ")
journey_start_time = get_input("Enter the journey start time (YYYY-MM-DD HH:MM:SS): ", validate_datetime)
journey_end_time = get_input("Enter the journey end time (YYYY-MM-DD HH:MM:SS): ", validate_datetime)
asset_id = get_input("Enter the asset id: ", validate_non_negative_int)
journey_arrival_zone = get_input("Enter the journey arrival zone (or leave blank for no parking): ", validate_arrival_zone_type)
journey_start_long = get_input("Enter the journey start longitude: ", validate_lat_or_long)
journey_start_lat = get_input("Enter the journey start latitude: ", validate_lat_or_long)
journey_end_long = get_input("Enter the journey end longitude: ", validate_lat_or_long)
journey_end_lat = get_input("Enter the journey end latitude: ", validate_lat_or_long)
journey_distance_travelled = get_input("Enter the distance travelled (metres) during journey: ", validate_float)
cur.execute('''INSERT INTO Journeys(rider_email, journey_start_time, journey_end_time, asset_id, journey_arrival_zone,
                                      journey_start_long, journey_start_lat, journey_end_long, journey_end_lat,
                                      journey_distance_travelled)
                VALUES(?,?,?,?,?,?,?,?,?,?)''',
            (rider_email, journey_start_time, journey_end_time, asset_id, journey_arrival_zone, journey_start_long,
             journey_start_lat, journey_end_long, journey_end_lat, journey_distance_travelled))
print("Data added to Journeys table.\n")

conn.commit()
conn.close()
