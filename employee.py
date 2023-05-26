# importing MySQL connector muodle
import mysql.connector as sqltor

mycon = sqltor.connect(host = "localhost", user="root",
                         password= "09142229277", 
                         database= "employees")

cursor = mycon.cursor()
# writing the query we want 
query = 'SELECT  * FROM info ORDER BY hight DESC, weight ASC;'
# executing the query
cursor.execute(query)

# printing the resulte
for (name, weight, hight) in cursor:
  print("{} {} {}".format(name, hight, weight))

# now the work is done so we close the cursor
mycon.close()