from sys import exit
from mysql.connector import errorcode
import mysql.connector
import re

# connecting to MySQL
cnx = mysql.connector.connect(host = "localhost", user="root",
                         password= "09142229277t")
cursor = cnx.cursor()

# DB_name stands for database name
DB_name = 'Email'
# defining Tablses as a dict because Tables in SQL is like dict's in python. it has keys and values
TABLES = {}
TABLES['person'] = ('CREATE TABLE person(username VARCHAR(300), password VARCHAR(20))')

# this is a function for creating a database useing python "no need for MySQL commands".
def create_database(cursor):
    try:
        cursor.execute('CREATE DATABASE {} DEFAULT CHARACTER SET ''utf8'.format(DB_name))
    except mysql.connector.connector.Error as err:
        print("Failed creatind database: {}".format(err))
        exit(1)

# this function is for detecting an error which is about not existing the database we want
def Error_detec(err):
    return err.errno == errorcode.ER_BAD_DB_ERROR

# this part changes to the database we want and if not it creates the database
try:
    cursor.execute("USE {}".format(DB_name))
except mysql.connector.Error as err:
    print("Database {} does not exist.".format(DB_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfuly".format(DB_name))
        cnx.database = DB_name
    else:
        print(err)
        exit(1)

# this part is for creating tables
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating Table {}: ".format(table_name), end="")
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# Cheking that the inputed email is valid or not
# regex is the regular tamplate for email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def email_check(email):
    if not(re.fullmatch(regex, email)):
        exit("Invalid Email. your email must be in this tamplate: expression@string.string")
        
get_info = input("Enter your Email: ")
email_check(get_info)

# Checking the inputed password in valid by the factors we have
def pass_check(passw):
    if len(passw) < 6 or len(passw) > 20:
        exit("Invalid Password. Password must be" 
                "at least 6 up to 20 characters")
    if not any(char.isdigit() for char in passw):
        exit("Invalid Password. Password must include at least one numeral.")
    if not any(char.isalpha() for char in passw):
        exit("Invalid Password. Password must include at least one letter.")
    else:
        return True

get_info_p = input("Enter your Password: ")
pass_check(get_info_p)

# Since we need to insert both email and password in a same row,
# we defined "info_list". "info_list" is a list which including "data_email" and "data_password"
info_list = []
data_email = get_info
data_password = get_info_p

info_list.append(data_email)
info_list.append(data_password)
print(info_list)
# Inserting the inputed data
add_info = ("INSERT INTO person (username, password) VALUES(%s, %s)")
cursor.execute(add_info, info_list)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()