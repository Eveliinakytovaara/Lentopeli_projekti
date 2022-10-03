"""
import mysql.connector

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='',
         password='',
         autocommit=True
         )

#Palauttaa muuttjuan matkan perusteella.
#“type” määrittää mitä palautetaan (lentokoneen koko vai kerroin)

#Parametri distance on float (kahden lentoaseman välinen matka) ja type string,
#joka määrittää mitä palautetaan ("size”, “mod”)

#distance = #take count from code
#sql = "SELECT * from player where trasvel_distance"
sql = "SELECT travel_distance from id, player "
print(sql)

cursor = connection.cursor()
cursor.execute(sql)

result = kursori.fetchall()

for line in result:
    print(f"{line[0]}, {line[1]}")
"""

#part 1
distance = int(input("Enter travel distance in km thousands: "))
min_distance = 1200
max_distance = 2500

if distance <= min_distance:
    print("plane small")

elif distance < max_distance and distance > min_distance:
    print("medium plane")

else:
    print("big plane")

#part2

distance = int(input("type distance: "))

if ?? <= distance < 1200:
    input_distance = float(input("type distance (km): "))
if distance >= 1200 or (distance>=?? and input_distance>=1200):
    print("you can fly.")
else:
    print("you cant fly.")