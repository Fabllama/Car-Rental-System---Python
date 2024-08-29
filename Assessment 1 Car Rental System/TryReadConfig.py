from read_config_file import Database

# Initialize the database connection
db = Database(config_filename='configfile.ini')

# Check connection and database setup
try:
    connection = db.create_connection_parser()
    print("Database and tables are properly set up.")
except Exception as e:
    print(f"An error occurred: {e}")
