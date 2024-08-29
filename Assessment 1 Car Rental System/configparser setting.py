import configparser

config = configparser.ConfigParser()

#add the structure to the file we will create
config.add_section('mysql')
config.set('mysql','host','localhost')
config.set('mysql','user','root')
config.set('mysql','password','root')
config.set('mysql','db','car_rental_db')

#write the new structure to a file using a relative path
with open("D:\\Visual Studio Projects\\Assessment 1 Car Rental System\\configfile.ini",'w') as configfile:
    config.write(configfile)