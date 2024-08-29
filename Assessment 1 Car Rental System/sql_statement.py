config_file = "configfile.ini"
default_db_name = "car_rental_db"
CREATE_DB = '''CREATE DATABASE IF NOT EXISTS car_rental_db'''
CREATE_USER_LOGIN_TABLE = '''CREATE TABLE IF NOT EXISTS user_login (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(45) NOT NULL UNIQUE,
    password VARCHAR(45) NOT NULL,
    type VARCHAR(45) NOT NULL,
    status ENUM('Y', 'N') NOT NULL DEFAULT 'Y'
)'''
CREATE_CARS_TABLE = '''CREATE TABLE IF NOT EXISTS cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    model_year INT NOT NULL,
    color VARCHAR(30),
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    daily_rate DECIMAL(10, 2) NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    status ENUM('Y', 'N') DEFAULT 'Y'
)'''
CREATE_CUSTOMER_TABLE = '''CREATE TABLE IF NOT EXISTS customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(45) NOT NULL UNIQUE,
    customer_name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    email VARCHAR(100) NOT NULL UNIQUE,
    mobile VARCHAR(15),
    FOREIGN KEY (username) REFERENCES user_login(username)
)'''
CREATE_RENTAL_REQUEST_TABLE = '''CREATE TABLE IF NOT EXISTS rental_request (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    car_id INT NOT NULL,
    rental_start_date DATE NOT NULL,
    rental_end_date DATE NOT NULL,
    daily_rate DECIMAL(10, 2),
    total_cost DECIMAL(10, 2),
    return_date DATE NULL,
    total_real_cost DECIMAL(10, 2) NULL,
    status ENUM('pending', 'approved', 'completed', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (car_id) REFERENCES cars(car_id))'''
TRY_LOGIN = '''SELECT type, user_id FROM user_login WHERE username = %s AND password = %s AND status = 'Y' '''
INSERT_USER = '''INSERT INTO user_login (username,password,type,status) VALUES (%s,%s,%s,'Y')'''
INSERT_CUSTOMER = '''INSERT INTO customer (username,customer_name,address,email,mobile) VALUES(%s,%s,%s,%s,%s)'''
INSERT_CAR = ''' INSERT INTO cars (model, model_year, color, license_plate, daily_rate, availability,status) VALUES (%s, %s, %s, %s, %s, %s,'Y') '''
SHOW_USER = '''SELECT * FROM user_login WHERE STATUS = 'Y' '''
SHOW_CAR = '''SELECT * FROM cars WHERE availability = 1 AND STATUS = 'Y' '''
SHOW_CAR_TO_RENT = ''' SELECT model, model_year, color, license_plate, daily_rate, availability FROM cars WHERE car_id = %s '''
SHOW_RENTAL_REQUEST = '''SELECT request_id, customer_id, car_id, rental_start_date, rental_end_date, daily_rate, total_cost, status FROM rental_request WHERE status = 'pending' '''
SHOW_RENTAL_HISTORY = '''SELECT * FROM rental_request'''
SHOW_RENTED_CAR_BY_USER = '''SELECT request_id, car_id, rental_start_date, rental_end_date, total_cost, status FROM rental_request WHERE customer_id = %s AND status IN ('pending','approved') '''
UPDATE_USER = ''' UPDATE user_login SET {fields} WHERE user_id = %s '''
UPDATE_CAR = '''UPDATE cars SET daily_rate = %s WHERE car_id = %s'''
DELETE_USER = '''UPDATE user_login SET STATUS = 'N' WHERE user_id = %s'''
DELETE_CAR = '''UPDATE cars SET STATUS = 'N' WHERE car_id = %s'''
NEW_REQUEST = ''' INSERT INTO rental_request (customer_id, car_id, rental_start_date, rental_end_date, daily_rate, total_cost, status) VALUES (%s, %s, %s, %s, %s, %s, 'pending') '''
APPROVE_REQUEST = ''' UPDATE rental_request SET status = 'approved' WHERE request_id = %s '''
REJECT_REQUEST = ''' UPDATE rental_request SET status = 'rejected' WHERE request_id = %s '''
COMPLETE_AND_UPDATE_REQUEST = '''UPDATE rental_request SET return_date = %s, total_real_cost = %s, status = 'completed' WHERE request_id = %s '''
GET_CUSTOMER_ID = '''SELECT customer_id FROM customer WHERE username = %s'''
GET_RENTED_CAR_DETAIL = '''SELECT rental_request.car_id, rental_request.rental_end_date, cars.daily_rate, rental_request.total_cost FROM rental_request JOIN cars ON rental_request.car_id = cars.car_id WHERE rental_request.request_id = %s AND rental_request.status != 'completed' '''
SET_CAR_UNAVAILABLE = '''UPDATE cars SET availability = 0 WHERE car_id = %s '''
SET_CAR_AVAILABLE = ''' UPDATE cars SET availability = 1 WHERE car_id = %s '''