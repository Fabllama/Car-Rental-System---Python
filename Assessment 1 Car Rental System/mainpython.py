from read_config_file import *

def main():
    #init database, check db+table exists
    if Database._init_database('configfile.ini') == False:
        Database._check_database_exist()
        Database._check_table_exist()
        Database.save_config()
    else:
        print("1. Login \n2. Exit")
        choice = int(input("Choice : "))
        if choice == 1:
            username=input("Enter username : ")
            password=input("Enter password : ")
            # if mycursor.execute(TRY_LOGIN,(username,password)) == None:
            #     quit
            # else:
            #     print("Welcome, ",username)
        else:
            quit


if __name__ == "__main__":
    main()