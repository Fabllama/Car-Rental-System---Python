import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="car_rental_db",
    autocommit = True #auto commit
)

mycursor = db.cursor()

#reset auto_increment
#mycursor.execute("alter table user_logins AUTO_INCREMENT = 1")

#create table
#mycursor.execute("create table user_logins (username varchar(15), password varchar(20), user_id int PRIMARY KEY AUTO_INCREMENT)")

#mycursor.execute("describe user_logins")
#this is for queries
#mycursor.execute()
sql = "INSERT INTO car_rental_db.user_logins (username,password) VALUES (%s,%s)",('fgh','fgh')
mycursor.execute(sql)
#mycursor.execute("truncate table user_logins")
#this is for commit data after insert queries
#db.commit()

mycursor.execute("select * from user_logins")

for x in mycursor:
    print(x)

#get all data
#mycursor.fetchall

#get one data, top one
#mycursor.fetchone