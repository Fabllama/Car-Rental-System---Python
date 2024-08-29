import configparser
import mysql.connector
from sql_statement import *

#load database configurations
# def load_config(filename='configfile.ini'):
#     config = configparser.ConfigParser()
#     config.read(filename)
#     return {key: value for key, value in config['mysql'].items()}

#database connection
# def create_connection_parser():
#     config=load_config

#     connection = mysql.connector.connect(**config, autocommit = True)

class Database:
    def __init__(self,config_filename):
        self.config_filename = config_file
        self.config_filename = None #hold connection object
        self._init_database()

    def _init_database(self):
        config = self.load_config()
        self.connection = mysql.connector.connect(**config,autocommit=True)
        if self.connection.is_connected():
            self._check_database_exist()
            self._check_table_exist()
            return True
        return False
    
    def create_connection_exist(self):
        config = self.load_config()
        if not config.get("database"):
            config['database'] = default_db_name
            self.save_config(config)

        cursor = self.create_connection_parser()
        cursor.execute(f"{CREATE_DB} {config['database']};")

    def _check_table_exist(self):
        cursor = self.create_connection_parser()
        cursor.execute(CREATE_USER_LOGIN_TABLE)

    def load_config(self):
        #load database configurations
        config = configparser.ConfigParser()
        config.read(self.config_filename)
        return{key:value for key, value in config['mysql'].items()}
    
    def save_config(self,config):
        #save database configurations to local
        config_parser = configparser.ConfigParser()
        config_parser['mysql'] = config
        #write the configuration to the file
        with open(self.config_filename, 'w') as configfile:
            configparser.write(configfile)
