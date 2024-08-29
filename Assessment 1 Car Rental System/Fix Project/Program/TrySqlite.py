import os
import sqlite3
from sqlite3 import Error
from sql_statement_lite import (CREATE_USER_LOGIN_TABLE, CREATE_CARS_TABLE,
                                CREATE_CUSTOMER_TABLE, CREATE_RENTAL_REQUEST_TABLE,
                                default_db_name,INSERT_USER,GET_ADMIN)

class Database:
    def __init__(self, db_filename=default_db_name):
        self.db_filename = db_filename
        self.connection = None
        self._create_database_file()
        self._init_database()

    def _create_database_file(self):
        """Create the SQLite database file if it does not exist."""
        if not os.path.isfile(self.db_filename):
            open(self.db_filename, 'w').close()

    def create_connection(self):
        """Create a new SQLite database connection and return the connection and cursor."""
        try:
            conn = sqlite3.connect(self.db_filename, isolation_level=None)  # Autocommit mode
            print(f"Connected to SQLite database at {self.db_filename}")
            return conn
        except Error as e:
            print(f"Error connecting to SQLite database: {e}")
            raise

    def _init_database(self):
        """Initialize the SQLite database and create tables if they do not exist."""
        self.connection = self.create_connection()
        self._check_table_exist()

    def _check_table_exist(self):
        """Check if tables exist and create them if they do not."""
        cursor = self.connection.cursor()
        try:
            table_queries = {
                'user_login': CREATE_USER_LOGIN_TABLE,
                'cars': CREATE_CARS_TABLE,
                'customer': CREATE_CUSTOMER_TABLE,
                'rental_request': CREATE_RENTAL_REQUEST_TABLE
            }
            for table_name, create_query in table_queries.items():
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                result = cursor.fetchone()
                if result:
                    print(f"Table '{table_name}' already exists.")
                else:
                    print(f"Table '{table_name}' does not exist. Creating...")
                    cursor.execute(create_query)
                    print(f"Table '{table_name}' created successfully.")
        except Error as e:
            print(f"Error checking or creating tables: {e}")
            raise
        finally:
            cursor.close()

    def generate_admin(self):
        """Generate admin user if it does not already exist."""
        admin_username = 'admin'
        
        if not self._admin_exists(admin_username):
            print(f"Admin user '{admin_username}' not found. Generating admin user.")
            try:
                with self.connection:  # Use the 'with' statement for the connection
                    cursor = self.connection.cursor()  # Create cursor manually
                    cursor.execute(INSERT_USER, (admin_username, 'admin', 'admin'))
                    print("Admin user inserted successfully.")
            except Error as e:
                print(f"Error inserting admin user: {e}")
        else:
            print(f"Admin user '{admin_username}' already exists.")

    def _admin_exists(self, username):
        """Check if an admin user exists in the user_login table."""
        #check_query = '''SELECT 1 FROM user_login WHERE username = ? AND type = 'admin' '''
        try:
            cursor = self.connection.cursor()  # Create cursor manually
            cursor.execute(GET_ADMIN, (username,))
            result = cursor.fetchone()
            cursor.close()  # Ensure cursor is closed
            return result is not None
        except Error as e:
            print(f"Error checking admin existence: {e}")
            return False