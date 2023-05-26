#Tested and Finished
from sys import exit
import requests
from mysql.connector import errorcode
import mysql.connector
from bs4 import BeautifulSoup

# Connecting to MySQL 
cnx = mysql.connector.connect(host = "localhost", user = "root" ,password= "09142229277t")
cursor = cnx.cursor()

car_model = input("Enter car module you want:")
# lowercaseing the car brand cause of URL 
car_model = car_model.lower()

# in the URL belowe, we insert the brand we want so we can request the main URL  
res = requests.get("https://www.truecar.com/used-cars-for-sale/listings/{}/location-brooklyn-ny/".format(car_model))

soup = BeautifulSoup(res.text, "html.parser")

# as websites codedings, we finde the price and miles amount
all_price = soup.find_all('div', attrs={'class' : 'heading-3 margin-y-1 font-weight-bold'}, limit= 20)
all_miles = soup.find_all('div', attrs={"data-test" : "vehicleMileage"}, limit= 20)


DB_name = 'Used_Cars_Price_and_Miles'

TABLES = {}
TABLES['car'] = ('CREATE TABLE car(Price CHAR(20), Miles CHAR(30))')

def creat_database(cursor):
    try:
        cursor.execute('CREATE DATABASE {} DEFAULT CHARACTER SET ''utf8'.format(DB_name))
    except mysql.connector.Error as err:
        print('Failed to creat database: {}'.format(err))
        exit(1)

# useing the database 
try:
    cursor.execute("USE {}".format(DB_name))
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        creat_database(cursor)
        print("Database {} successfuly created".format(DB_name))
        cnx.database = DB_name
    else:
        print(err)
        exit(1)

# createing tables in database
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating Table {}".format(table_name))
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists")
        else:
            print(err.msg)
    else:
        print("OK")

# appendding prices and miles amount to lists
price_list = []
for price in all_price:
    price_text = price.text    
    price_list.append(price_text)

miles_list = []
for miles in all_miles:
    miles_text = miles.text
    miles_list.append(miles_text)

# one by one, we make a list "info_list" wich has to elements for inserting them to the table.
# first element is prices and the second one is for miles. two by two, all synceed, we add tthem to table.
for i in range(20):
    info_list = []
    info_list.append(price_list[i])
    info_list.append(miles_list[i])
    print(info_list)
    add_price = ("INSERT INTO car(Price, Miles) VALUES( %s, %s)")
    cursor.execute(add_price, info_list)

# ensureing datas are inserted
cnx.commit()

# closeing MySQL
cursor.close()
cnx.close()