default_db_name = "car_rental_db.sqlite"
CREATE_DB = '''CREATE DATABASE IF NOT EXISTS car_rental_db'''
CREATE_USER_LOGIN_TABLE = '''CREATE TABLE IF NOT EXISTS user_login (
    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Y'
)'''

CREATE_CARS_TABLE = '''CREATE TABLE IF NOT EXISTS cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    model_year INTEGER NOT NULL,
    color TEXT,
    license_plate TEXT UNIQUE NOT NULL,
    daily_rate REAL NOT NULL,
    availability BOOLEAN DEFAULT 1,
    status TEXT DEFAULT 'Y'
)'''

CREATE_CUSTOMER_TABLE = '''CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    customer_name TEXT NOT NULL,
    address TEXT,
    email TEXT NOT NULL UNIQUE,
    mobile TEXT,
    FOREIGN KEY (username) REFERENCES user_login(username)
)'''

CREATE_RENTAL_REQUEST_TABLE = '''CREATE TABLE IF NOT EXISTS rental_request (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    rental_start_date DATE NOT NULL,
    rental_end_date DATE NOT NULL,
    daily_rate REAL,
    total_cost REAL,
    return_date DATE,
    total_real_cost REAL,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (car_id) REFERENCES cars(car_id)
)'''
TRY_LOGIN = '''SELECT type, user_id FROM user_login WHERE username = ? AND password = ? AND status = 'Y' '''
INSERT_USER = '''INSERT INTO user_login (username, password, type, status) VALUES (?, ?, ?, 'Y')'''
INSERT_CUSTOMER = '''INSERT INTO customer (username, customer_name, address, email, mobile) VALUES (?, ?, ?, ?, ?)'''
INSERT_CAR = '''INSERT INTO cars (model, model_year, color, license_plate, daily_rate, availability, status) VALUES (?, ?, ?, ?, ?, ?, 'Y')'''
SHOW_USER = '''SELECT * FROM user_login WHERE status = 'Y' '''
SHOW_CAR = '''SELECT * FROM cars WHERE availability = 1 AND status = 'Y' '''
SHOW_CAR_TO_RENT = '''SELECT model, model_year, color, license_plate, daily_rate, availability FROM cars WHERE car_id = ?'''
SHOW_RENTAL_REQUEST = '''SELECT request_id, customer_id, car_id, rental_start_date, rental_end_date, daily_rate, total_cost, status FROM rental_request WHERE status = 'pending' '''
SHOW_RENTAL_HISTORY = '''SELECT * FROM rental_request'''
SHOW_RENTED_CAR_BY_USER = '''SELECT request_id, car_id, rental_start_date, rental_end_date, total_cost, status FROM rental_request WHERE customer_id = ? AND status IN ('pending', 'approved') '''
UPDATE_USER = '''UPDATE user_login SET {fields} WHERE user_id = ?'''
UPDATE_CAR = '''UPDATE cars SET daily_rate = ? WHERE car_id = ?'''
DELETE_USER = '''UPDATE user_login SET status = 'N' WHERE user_id = ?'''
DELETE_CAR = '''UPDATE cars SET status = 'N' WHERE car_id = ?'''
NEW_REQUEST = '''INSERT INTO rental_request (customer_id, car_id, rental_start_date, rental_end_date, daily_rate, total_cost, status) VALUES (?, ?, ?, ?, ?, ?, 'pending')'''
APPROVE_REQUEST = '''UPDATE rental_request SET status = 'approved' WHERE request_id = ?'''
REJECT_REQUEST = '''UPDATE rental_request SET status = 'rejected' WHERE request_id = ?'''
COMPLETE_AND_UPDATE_REQUEST = '''UPDATE rental_request SET return_date = ?, total_real_cost = ?, status = 'completed' WHERE request_id = ?'''
GET_ADMIN = '''SELECT 1 FROM user_login WHERE username = ? AND type = 'admin' '''
GET_CUSTOMER_ID = '''SELECT customer_id FROM customer WHERE username = ?'''
GET_CAR_ID = '''SELECT car_id FROM rental_request WHERE request_id = ?'''
GET_CAR_AVAILABILITY = '''SELECT daily_rate, availability FROM cars WHERE car_id = ?'''
GET_RENTED_CAR_DETAIL = '''SELECT rental_request.car_id, rental_request.rental_end_date, cars.daily_rate, rental_request.total_cost FROM rental_request JOIN cars ON rental_request.car_id = cars.car_id WHERE rental_request.request_id = ? AND rental_request.status != 'completed' '''
GET_RENTAL_REQUEST_STATUS = '''SELECT status FROM rental_request WHERE request_id = ?'''
GET_RENTAL_STATUS = '''SELECT status FROM rental_request WHERE request_id = ?'''
SET_CAR_UNAVAILABLE = '''UPDATE cars SET availability = 0 WHERE car_id = ?'''
SET_CAR_AVAILABLE = '''UPDATE cars SET availability = 1 WHERE car_id = ?'''