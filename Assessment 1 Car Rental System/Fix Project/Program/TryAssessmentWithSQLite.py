# main_script.py
import sqlite3
from TrySqlite import Database
from sql_statement_lite import *
from sqlite3 import Error
from datetime import datetime

def verify_user(cursor, username, password):
    """Verify a user's credentials and return their type and user_id."""
    try:
        # Query to verify username and password
        #try_log = '''SELECT type, user_id FROM user_login WHERE username = ? AND password = ? AND status = 'Y' '''
        
        cursor.execute(TRY_LOGIN, (username, password))
        row = cursor.fetchone()

        if row:
            user_type, user_id = row
            
            if user_type == 'admin':
                # If the user is an admin, return None for customer_id
                return user_type, None
            
            elif user_type == 'member':
                # Query to get customer_id based on username
                #sql_get_customer_id = '''SELECT customer_id FROM customer WHERE username = ?'''
                cursor.execute(GET_CUSTOMER_ID, (username,))
                customer_row = cursor.fetchone()

                if customer_row:
                    customer_id = customer_row[0]
                    # Return the user type and customer_id
                    return user_type, customer_id
                else:
                    return None, None  # Customer ID not found
            
        else:
            return None, None  # Credentials invalid
        
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None, None  # Return None in case of any error

def execute_query(connection, query, params=None, fetchone=False, fetchall=False):
    """Utility function to execute a query with optional parameters and fetch results if needed."""
    try:
        with connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if fetchone:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()
            #conn.commit()
    except Error as e:
        print(f"Error executing query: {e}")
        return None

class AdminMenu:
    def __init__(self, connection):
        # Initialize the AdminMenu with a database connection and cursor.
        self.connection = connection
        self.user_management = UserManagement(connection)
        self.cars_management = CarsManagement(connection)
        self.rent_management = RentManagement(connection)

    def display_admin_menu(self):
        # Display the admin menu and handle user choices.
        while True:
            print("\n--- Admin Menu ---")
            print("1. Manage users")
            print("2. Manage cars")
            print("3. Manage rent requests")
            print("4. Logout")

            try:
                admin_choice = int(input("Enter choice = "))
            except ValueError:
                print("Invalid input! Please enter a number.\n")
                continue

            if admin_choice == 1:
                self.user_management.display_manage_users_menu()
            elif admin_choice == 2:
                self.cars_management.display_manage_cars_menu()
            elif admin_choice == 3:
                self.rent_management.display_rent_requests_menu()
            elif admin_choice == 4:
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 4.\n")

class UserManagement:
    def __init__(self, connection):
        # Initialize the UserManagement with a database connection.
        self.connection = connection

    def add_user(self):
        # Add a new user to the database.
        new_username = input("Input username: ")
        new_password = input("Input password: ")

        print("Select role:")
        print("1. Admin")
        print("2. Member")
        role = input("Enter role (1/2): ")

        if role == '1':
            new_role = 'admin'
            values = (new_username, new_password, new_role)
            sql = INSERT_USER

            try:
                execute_query(self.connection, sql, values)
                print("New admin user added successfully.\n")
            except Error as e:
                print(f"Error adding user: {e}\n")
        
        elif role == '2':
            new_role = 'member'
            customer_name = input("Input name: ")
            customer_address = input("Input address: ")
            customer_email = input("Input email: ")
            customer_mobile = input("Input mobile number: ")

            sql1 = INSERT_USER
            values1 = (new_username, new_password, new_role)

            sql2 = INSERT_CUSTOMER
            values2 = (new_username, customer_name, customer_address, customer_email, customer_mobile)

            try:
                execute_query(self.connection, sql1, values1)
                execute_query(self.connection, sql2, values2)
                print("New member user added successfully.\n")
            except Error as e:
                print(f"Error adding user: {e}\n")
        
        else:
            print("Invalid role! User not added.\n")

    def edit_user(self):
        # Edit an existing user in the database.
        try:
            # Get and display existing users
            sql = SHOW_USER
            users = execute_query(self.connection, sql, fetchall=True)

            if not users:
                print("No users found to edit.\n")
                return

            print("Existing users:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")

            # Get the ID of the user to edit
            user_id = input("Enter the ID of the user to edit (leave blank to cancel): ")

            if not user_id:
                print("Operation canceled")
                return

            if not any(user[0] == int(user_id) for user in users):
                print("User ID not found.\n")
                return

            # Get new details for the user
            new_username = input("Enter new username (blank to keep current): ")
            new_password = input("Enter new password (blank to keep current): ")
            new_role = input("Enter new role (admin/member, blank to keep current): ")

            update_fields = []
            update_values = []

            if new_username:
                update_fields.append("username = ?")
                update_values.append(new_username)
            if new_password:
                update_fields.append("password = ?")
                update_values.append(new_password)
            if new_role:
                if new_role.lower() not in ['admin', 'member']:
                    print("Invalid role. User not updated.\n")
                    return
                update_fields.append("role = ?")
                update_values.append(new_role.lower())

            if not update_fields:
                print("No changes were made.\n")
                return

            update_values.append(user_id)
            sql = f"UPDATE user_login SET {', '.join(update_fields)} WHERE id = ?"
            execute_query(self.connection, sql, tuple(update_values))
            print("User updated successfully.\n")

        except Error as e:
            print(f"Error editing user: {e}\n")

    def delete_user(self):
        # Delete (deactivate) an existing user in the database.
        try:
            # Get and display existing users
            sql = SHOW_USER
            users = execute_query(self.connection, sql, fetchall=True)

            if not users:
                print("No users found to delete.\n")
                return

            print("Existing users:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")

            user_id = input("Enter the ID of the user to delete: ")

            try:
                user_id_int = int(user_id)
            except ValueError:
                print("Operation canceled.\n")
                return

            if not any(user[0] == user_id_int for user in users):
                print("User ID not found.\n")
                return

            sql = DELETE_USER
            execute_query(self.connection, sql, (user_id,))
            print("User deleted successfully.\n")

        except Error as e:
            print(f"Error deleting user: {e}\n")

    def display_manage_users_menu(self):
        # Display the user management menu and handle user choices.
        while True:
            print("\nUser Management Menu:")
            print("1. Add new user")
            print("2. Edit user")
            print("3. Delete user")
            print("4. Back to Admin menu")

            try:
                choice = int(input("Enter choice = "))
            except ValueError:
                print("Invalid input! Please enter a number.\n")
                continue

            if choice == 1:
                self.add_user()
            elif choice == 2:
                self.edit_user()
            elif choice == 3:
                self.delete_user()
            elif choice == 4:
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 4.\n")

class CarsManagement:
    def __init__(self, connection):
        # Initialize the CarsManagement with a database connection.
        self.connection = connection

    def add_car(self):
        # Add a new car to the database.
        car_model = input("Enter car model: ")
        car_model_year = input("Enter car model year: ")
        car_color = input("Enter car color: ")
        car_license_plate = input("Enter car license plate: ")
        car_daily_rate = input("Enter car daily rate: ")

        # Validate and convert inputs to the correct types
        try:
            car_model_year = int(car_model_year)
            car_daily_rate = float(car_daily_rate)
        except ValueError:
            print("Invalid input for model year or daily rate.\n")
            return

        sql = INSERT_CAR
        values = (car_model, car_model_year, car_color, car_license_plate, car_daily_rate, True)

        try:
            execute_query(self.connection, sql, values)
            print("New car added successfully.\n")
        except Error as e:
            print(f"Error adding car: {e}\n")

    def edit_car(self):
        # Edit the daily rate of an existing car.
        try:
            # Fetch and display existing cars
            sql = SHOW_CAR
            cars = execute_query(self.connection, sql, fetchall=True)

            if not cars:
                print("No cars found to edit.\n")
                return

            print("Existing cars:")
            for car in cars:
                print(f"ID: {car[0]}, Model: {car[1]}, Year: {car[2]}, Color: {car[3]}, License Plate: {car[4]}, Daily Rate: {car[5]}")

            # Get the ID of the car to edit
            car_id = input("Enter the ID of the car to update the daily rate (leave blank to cancel): ")

            if not car_id:
                print("Operation canceled.\n")
                return

            # Validate if the car exists
            if not any(car[0] == int(car_id) for car in cars):
                print("Car ID not found.\n")
                return

            # Get new daily rate from the user
            new_daily_rate = input("Enter new daily rate (blank to keep current): ")

            if not new_daily_rate:
                print("No changes made.\n")
                return

            try:
                new_daily_rate = float(new_daily_rate)
                if new_daily_rate < 0:
                    raise ValueError("Daily rate must be a positive number.")
            except ValueError as ve:
                print(f"Invalid daily rate: {ve}\n")
                return

            sql = UPDATE_CAR
            values = (new_daily_rate, car_id)

            execute_query(self.connection, sql, values)
            print("Daily rate updated successfully.\n")

        except Error as e:
            print(f"Error editing car: {e}\n")

    def delete_car(self):
        # Delete an existing car from the database.
        try:
            # Fetch and display existing cars
            sql = SHOW_CAR
            cars = execute_query(self.connection, sql, fetchall=True)

            if not cars:
                print("No cars found to delete.\n")
                return

            print("Existing cars:")
            for car in cars:
                print(f"ID: {car[0]}, Model: {car[1]}, Year: {car[2]}, Color: {car[3]}, License Plate: {car[4]}, Daily Rate: {car[5]}")

            # Get the ID of the car to delete
            car_id = input("Enter the ID of the car to delete: ")

            # Handle if left blank to cancel operation
            try:
                car_id_int = int(car_id)
            except ValueError:
                print("Operation canceled.\n")
                return

            # Validate if the car exists
            if not any(car[0] == car_id_int for car in cars):
                print("Car ID not found.\n")
                return

            sql = DELETE_CAR
            values = (car_id,)

            execute_query(self.connection, sql, values)
            print("Car deleted successfully.\n")

        except Error as e:
            print(f"Error deleting car: {e}\n")

    def display_manage_cars_menu(self):
        # Display the car management menu and handle user choices.
        while True:
            print("\nManage Cars Menu:")
            print("1. Add new car")
            print("2. Edit car")
            print("3. Delete car")
            print("4. Back to Admin menu")

            try:
                choice = int(input("Enter choice = "))
            except ValueError:
                print("Invalid input! Please enter a number.\n")
                continue

            if choice == 1:
                self.add_car()
            elif choice == 2:
                self.edit_car()
            elif choice == 3:
                self.delete_car()
            elif choice == 4:
                break  # Return to Admin menu
            else:
                print("Invalid choice! Please enter a number between 1 and 4.\n")

class RentManagement:
    def __init__(self, connection):
        # Initialize the RentManagement with a database connection.
        self.connection = connection

    def view_rent_requests(self):
        # View all rental requests.
        sql = SHOW_RENTAL_REQUEST
        try:
            requests = execute_query(self.connection, sql, fetchall=True)
            
            if requests:
                for request in requests:
                    print(f"Request ID: {request[0]}, Customer ID: {request[1]}, Car ID: {request[2]}, Start Date: {request[3]}, End Date: {request[4]}, Daily Rate: {request[5]}, Total Cost: {request[6]}, Status: {request[7]}")
            else:
                print("No rental requests found.\n")
        except Error as e:
            print(f"Error retrieving rental requests: {e}\n")

    def approve_rent_request(self):
        # Approve a specific rent request.
        try:
            # Fetch and display existing rent requests with status 'pending'
            requests = execute_query(self.connection, SHOW_RENTAL_REQUEST, fetchall=True)

            if not requests:
                print("No pending rent requests to approve.\n")
                return

            print("Pending rent requests:")
            for request in requests:
                print(f"ID: {request[0]}, Customer ID: {request[1]}, Car ID: {request[2]}, Start Date: {request[3]}, End Date: {request[4]}")

            # Get the ID of the request to approve
            request_id = input("Enter the ID of the rent request to approve: ").strip()

            if not request_id:
                print("Operation canceled.\n")
                return

            # Check if the request ID exists in the list of pending requests
            if not any(str(request[0]) == request_id for request in requests):
                print("Request ID not found.\n")
                return

            # Fetch the car_id associated with the request_id
            car_id_row = execute_query(self.connection, GET_CAR_ID, (request_id,), fetchone=True)
            
            if not car_id_row:
                print("Error: Car ID not found for the specified request.\n")
                return

            car_id = car_id_row[0]

            # Update the status of the rental request
            execute_query(self.connection, APPROVE_REQUEST, (request_id,))

            # Update the availability of the car
            execute_query(self.connection, SET_CAR_UNAVAILABLE, (car_id,))

            print("Rent request approved and car availability updated successfully.\n")

        except Error as e:
            # Rollback the transaction if there's an error
            self.connection.rollback()
            print(f"Error processing rent request: {e}\n")

    def reject_rent_request(self):
        # Reject a specific rent request.
        try:
            # Fetch and display existing rent requests with status 'pending'
            requests = execute_query(self.connection, SHOW_RENTAL_REQUEST, fetchall=True)

            if not requests:
                print("No pending rent requests to reject.\n")
                return

            print("Pending rent requests:")
            for request in requests:
                print(f"ID: {request[0]}, Customer ID: {request[1]}, Car ID: {request[2]}, Start Date: {request[3]}, End Date: {request[4]}")

            # Get the ID of the request to reject
            request_id = input("Enter the ID of the rent request to reject: ").strip()

            if not request_id:
                print("Operation canceled.\n")
                return

            # Check if the request ID exists in the list of pending requests
            if not any(str(request[0]) == request_id for request in requests):
                print("Request ID not found.\n")
                return

            # Fetch the car_id associated with the request_id
            car_id_row = execute_query(self.connection, GET_CAR_ID, (request_id,), fetchone=True)

            if not car_id_row:
                print("Error: Car ID not found for the specified request.\n")
                return

            car_id = car_id_row[0]

            # Update the status of the rental request
            execute_query(self.connection, REJECT_REQUEST, (request_id,))

            # Update the availability of the car
            execute_query(self.connection, SET_CAR_AVAILABLE, (car_id,))

            print("Rent request rejected and car is now available.\n")

        except Error as e:
            # Rollback the transaction if there's an error
            self.connection.rollback()
            print(f"Error processing rent request: {e}\n")

    def view_rent_history(self):
        # View the rental history.
        sql = SHOW_RENTAL_HISTORY
        try:
            history = execute_query(self.connection, sql, fetchall=True)
            
            if history:
                for record in history:
                    print(f"Request ID: {record[0]}, Customer ID: {record[1]}, Car ID: {record[2]}, Start Date: {record[3]}, End Date: {record[4]}, Daily Rate: {record[5]}, Total Cost: {record[6]}, Return Date: {record[7]}, Total Real Cost: {record[8]}, Status: {record[9]}")
            else:
                print("No rental history found.\n")
        except Error as e:
            print(f"Error retrieving rental history: {e}\n")

    def display_rent_requests_menu(self):
        # Display the rent requests management menu and handle user choices.
        while True:
            print("\nRent Requests Management Menu:")
            print("1. View rent requests")
            print("2. Approve rent request")
            print("3. Reject rent request")
            print("4. View rent history")
            print("5. Back to Admin menu")

            try:
                choice = int(input("Enter choice = "))
            except ValueError:
                print("Invalid input! Please enter a number.\n")
                continue

            if choice == 1:
                self.view_rent_requests()
            elif choice == 2:
                self.approve_rent_request()
            elif choice == 3:
                self.reject_rent_request()
            elif choice == 4:
                self.view_rent_history()
            elif choice == 5:
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 5.\n")

class MemberMenu:
    def __init__(self, connection, customer_id):
        # Initialize the MemberMenu with a database connection and customer ID.
        self.connection = connection
        self.cursor = connection.cursor()
        self.customer_id = customer_id

    def display_member_menu(self):
        # Display the menu for the member and handle invalid inputs.
        while True:
            print("\n--- Member Menu ---")
            print("1. See Car List")
            print("2. Rent a Car")
            print("3. Return a Car")
            print("4. See Request Status")
            print("5. Logout")
            
            try:
                choice = int(input("Enter your choice: ").strip())
                
                if choice == 1:
                    self.see_car_list()
                elif choice == 2:
                    self.rent_car()
                elif choice == 3:
                    self.return_car()
                elif choice == 4:
                    self.see_request_status()
                elif choice == 5:
                    print("Exiting menu.")
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number from the member menu options.")

    def see_car_list(self):
        # Display the list of available cars.
        sql = SHOW_CAR
        try:
            cars = execute_query(self.connection, sql, fetchall=True)
            
            if cars:
                print("\nAvailable Cars:")
                for car in cars:
                    print(f"ID: {car[0]}, Model: {car[1]}, Year: {car[2]}, Color: {car[3]}, License Plate: {car[4]}, Daily Rate: {car[5]}")
            else:
                print("No cars are available at the moment.\n")
        except Error as e:
            print(f"Error fetching car list: {e}\n")

    def rent_car(self):
        # Handle the process of renting a car.
        car_id = input("Enter the ID of the car you want to rent (or press Enter to cancel): ").strip()
        if not car_id:
            print("Operation canceled.\n")
            return
        
        rental_start_date = input("Enter rental start date (YYYY-MM-DD, or press Enter to cancel): ").strip()
        if not rental_start_date:
            print("Operation canceled.\n")
            return
        
        rental_end_date = input("Enter rental end date (YYYY-MM-DD, or press Enter to cancel): ").strip()
        if not rental_end_date:
            print("Operation canceled.\n")
            return

        try:
            # Change the date format into correct format (YYYY-MM-DD)
            start_date_dt = datetime.strptime(rental_start_date, "%Y-%m-%d").date()
            end_date_dt = datetime.strptime(rental_end_date, "%Y-%m-%d").date()
            
            # Get car details
            car = execute_query(self.connection, GET_CAR_AVAILABILITY, (car_id,), fetchone=True)
            
            if not car:
                print("Car does not exist.\n")
                return
            
            daily_rate, availability = car
            
            if availability == 0:
                print("Car not available.\n")
                return
            
            # Calculate rental duration
            if start_date_dt >= end_date_dt:
                print("End date must be after start date.\n")
                return

            total_days = (end_date_dt - start_date_dt).days
            if total_days <= 0:
                print("Invalid rental period.\n")
                return
            
            total_cost = daily_rate * total_days
            
            values = (self.customer_id, car_id, rental_start_date, rental_end_date, daily_rate, total_cost)
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(NEW_REQUEST, values)
                request_id = cursor.lastrowid
            
            execute_query(self.connection, SET_CAR_UNAVAILABLE, (car_id,))
            
            print(f"Car rented successfully.\nRequest ID: {request_id}\n")
        except ValueError as e:
            print(f"Invalid date format: {e}. Please use YYYY-MM-DD.\n")
        except Exception as e:
            print(f"Error renting car: {e}\n")

    def return_car(self):
        # Handle the return of a rented car.
        try:
            # List all rented cars that are not completed
            rented_cars = execute_query(self.connection, SHOW_RENTED_CAR_BY_USER, (self.customer_id,), fetchall=True)

            if not rented_cars:
                print("No cars to return or all cars have been returned.\n")
                return
            
            print("Rented Cars:")
            for rental in rented_cars:
                request_id, car_id, rental_start_date, rental_end_date, total_cost, status = rental

                # Format dates for display (already in YYYY-MM-DD format)
                rental_start_date_str = rental_start_date if rental_start_date else "N/A"
                rental_end_date_str = rental_end_date if rental_end_date else "N/A"
                
                print(f"Request ID: {request_id}, Car ID: {car_id}, Start Date: {rental_start_date_str}, End Date: {rental_end_date_str}, Total Cost: {total_cost}, Status: {status}")
            
            # Get the request ID for the return
            request_id = input("Enter the ID of the rental request to return (or press Enter to cancel): ").strip()
            if not request_id:
                print("Operation canceled.\n")
                return

            # Check if the request is approved
            if not self.check_approved_request(request_id):
                print("Cannot return this car as the request is either pending or already completed.\n")
                return

            # Get the return date
            return_date_str = input("Enter return date (YYYY-MM-DD): ").strip()
            if not return_date_str:
                print("Operation canceled.\n")
                return

            # Validate return date format
            try:
                datetime.strptime(return_date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.\n")
                return
            
            # Get rental request details
            request_car = execute_query(self.connection, GET_RENTED_CAR_DETAIL, (request_id,), fetchone=True)

            if not request_car:
                print("Rental request not found or already completed.\n")
                return

            car_id, rental_end_date, daily_rate, total_cost = request_car

            # Convert rental_end_date and return_date to datetime.date objects for comparison
            try:
                rental_end_date_str = datetime.strptime(rental_end_date, "%Y-%m-%d").date()
                return_date_str = datetime.strptime(return_date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Error processing dates.\n")
                return

            # Calculate the number of days late
            days_late = (return_date_str - rental_end_date_str).days

            if days_late < 0:
                print("Return date cannot be earlier than the rental end date.\n")
                return

            # Calculate total real cost
            total_real_cost = (days_late * daily_rate) + total_cost

            # Format return date for SQL
            formatted_return_date = return_date_str.strftime("%Y-%m-%d")

            # Update rental request with return date and total real cost
            execute_query(self.connection, COMPLETE_AND_UPDATE_REQUEST, (formatted_return_date, total_real_cost, request_id))

            # Update car availability
            execute_query(self.connection, SET_CAR_AVAILABLE, (car_id,))

            print(f"Car returned successfully. Your total cost: {total_real_cost}\n")
        except Exception as e:
            self.connection.rollback()
            print(f"Error returning car: {e}\n")

    def check_approved_request(self, request_id):
        #Check if the rental request is approved or pending.
        try:
            self.cursor.execute(GET_RENTAL_STATUS, (request_id,))
            result = self.cursor.fetchone()

            if result:
                status = result[0]
                if status == 'pending':
                    return False  # Cannot return if pending
                elif status == 'approved':
                    return True  # Can return if approved
            return False  # Return False if request does not exist or is already completed
        except Exception as e:
            print(f"Error checking request status: {e}")
            return False

    def see_request_status(self):
        #Show the status of the member's rental requests.
        try:
            self.cursor.execute(SHOW_RENTED_CAR_BY_USER, (self.customer_id,))
            requests = self.cursor.fetchall()

            if requests:
                print("\nYour Rental Requests:")
                for request in requests:
                    request_id, car_id, rental_start_date, rental_end_date, total_cost, status = request
                    
                    # Directly use the date strings retrieved from the database
                    rental_start_date_str = rental_start_date if rental_start_date else "N/A"
                    rental_end_date_str = rental_end_date if rental_end_date else "N/A"

                    # Print request details
                    print(f"ID: {request_id}, Car ID: {car_id}, Start Date: {rental_start_date_str}, End Date: {rental_end_date_str}, Total Cost: {total_cost:.2f}, Status: {status}")
            else:
                print("No rental requests found.\n")
        except Exception as e:
            print(f"Error retrieving rental requests: {e}\n")

def main():
    # Initialize the database with the SQLite database file
    db = Database(default_db_name)  # Use SQLite file extension
    
    # Generate admin user
    db.generate_admin()
    
    # Get the connection from the Database class
    connection = db.connection
    
    # Create an AdminMenu instance
    admin_menu = AdminMenu(connection)
    
    while True:
        print("\n1. Login")
        print("2. Quit")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.\n")
            continue

        if choice == 1:
            # Login process
            username = input("Username: ")
            password = input("Password: ")

            # Create a cursor for executing queries
            cursor = connection.cursor()
            try:
                user_type, user_id = verify_user(cursor, username, password)
                
                if user_type:
                    if user_type == 'admin':
                        print(f"\nLogin successful! Welcome, Admin {username}")
                        admin_menu.display_admin_menu()
                    elif user_type == 'member':
                        print(f"\nLogin successful! Welcome, {username}")
                        # Initialize MemberMenu with the user_id
                        member_menu = MemberMenu(connection, user_id)
                        member_menu.display_member_menu()
                    else:
                        print("User type not recognized.")
                else:
                    print("Invalid username or password. Please try again.")
            except Exception as e:
                print(f"An error occurred during login: {e}")
            finally:
                # Ensure the cursor is closed after use
                cursor.close()

        elif choice == 2:
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please select a valid option.")
    
    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()
