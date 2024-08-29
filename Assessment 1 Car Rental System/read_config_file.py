import os
import configparser
import mysql.connector
from mysql.connector import Error
from sql_statement import *

class Database:
    def __init__(self, config_filename):
        self.config_filename = config_filename
        self.connection = None
        self._create_default_config()
        self._init_database()

    def _create_default_config(self):
        """Create a default configuration file if it does not exist."""
        if not os.path.isfile(self.config_filename):
            config = configparser.ConfigParser()
            config['mysql'] = {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'database': 'car_rental_db'
            }
            self.save_config(config)

    def load_config(self):
        """Load database configurations from an INI file."""
        config = configparser.ConfigParser()
        config.read(self.config_filename)
        return {key: value for key, value in config['mysql'].items()}

    def save_config(self, config):
        """Save database configurations to an INI file."""
        config_parser = configparser.ConfigParser()
        config_parser['mysql'] = config
        with open(self.config_filename, 'w') as configfile:
            config_parser.write(configfile)

    def _init_database(self):
        """Initialize the database and check if the database and tables exist."""
        config = self.load_config()
        if self._check_server_connection():
            self.connection = mysql.connector.connect(**config, autocommit=True)
            if self.connection.is_connected():
                self._check_database_exist()
                self._check_table_exist()
            else:
                raise Exception("Failed to connect to the database.")
        else:
            raise Exception("Failed to connect to MySQL server.")

    def _check_server_connection(self):
        """Check if a connection to the MySQL server can be established."""
        config = self.load_config()
        try:
            # Attempt to connect to MySQL server without specifying a database
            test_connection = mysql.connector.connect(
                host=config.get('host', 'localhost'),
                user=config.get('user', 'root'),
                password=config.get('password', 'root'),
                autocommit=True
            )
            if test_connection.is_connected():
                test_connection.close()
                print("Successfully connected to MySQL server.")
                return True
        except Error as e:
            print(f"Error connecting to MySQL server: {e}")
        return False

    def _check_database_exist(self):
        """Create the database if it does not exist."""
        config = self.load_config()
        db_name = config.get('database', 'car_rental_db')
        if not db_name:
            config['database'] = 'car_rental_db'
            self.save_config(config)
            db_name = 'car_rental_db'

        cursor = self.create_connection_parser()
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"Database '{db_name}' is available.")
        finally:
            cursor.close()

    def _check_table_exist(self):
        """Create tables if they do not exist."""
        cursor = self.create_connection_parser()
        try:
            table_queries = {
                'user_login': CREATE_USER_LOGIN_TABLE,
                'cars': CREATE_CARS_TABLE,
                'customer': CREATE_CUSTOMER_TABLE,
                'rental_request': CREATE_RENTAL_REQUEST_TABLE
            }
            for table_name, create_query in table_queries.items():
                cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
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

    def create_connection_parser(self):
        """Create a new database connection and return a cursor."""
        config = self.load_config()
        self.connection = mysql.connector.connect(**config, autocommit=True)

        if self.connection.is_connected():
            return self.connection.cursor()
        else:
            raise Exception("Failed to create a database connection.")
