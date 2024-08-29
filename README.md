# Car Rental Management System

## Overview

This project is a Car Rental Management System that includes functionality for both administrators and customers. The system is designed to manage users, cars, rent requests, and maintain records of all transactions. The project consists of Python classes for handling various aspects of the system, including user management, car management, rental management and a transaction made by customers.

## Admin Features
### Manage Users
  - **Add User**
    - Addng user (admin/customer) : Default admin username is admin, and yes customer need to contact employee to create new account/username.
  - **Edit User**
    - Editing existing user : Change username or password or role (just incase the customer now work in the company as an admin).
  - **Delete User**
    - Delete any existing user : Delete any user.
### Manage Cars
  - **Add Car**
    - Addng car : Add new car data such as model, year model, license plate, etc.
  - **Edit Car**
    - Editing existing car : Change daily rate for specific car.
  - **Delete Car**
    - Delete any existing car : Delete any car.
### Manage Rent Requests
  - **View rent requests**
    - View all pending request(s)
  - **Approve request**
    - Approve any selected request
  - **Reject request**
    - Reject any selected request
  - **View request history**
    - View all request history, including all details like the total rent, rent date, return date, etc.

## Customer Features
- **View Car List**
  - Browse all available cars.
- **Rent Car**
  - Request to rent a car.
- **Return Car**
  - Return rented cars. If the return date is more than the "End date" (the promised date to return the car) then the program will calculate the actual rent cost.
- **See Request Status**
  - Check the status of the car rental request.

## Prerequisites
- Python 3.x
- SQLite

## Installation
1. No need to install, just get a copy and ready to go~
   ```bash
   git clone https://github.com/Fabllama/Car-Rental-System---Python.git
