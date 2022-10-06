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

# part 1
distance = int(input("Enter travel distance in km thousands: "))
min_distance = 1200
max_distance = 2500


def get_plane(_distance, _type):
    if _distance <= min_distance:
        if _type == "name":
            return "small plane"
        else:
            return "0.75"

    elif max_distance > _distance > min_distance:
        if _type == "name":
            return "medium plane"
        else:
            return "1.5"

    else:
        if _type == "name":
            return "big plane"
        else:
            return "2.0"

# part2
'''
distance = int(input("type distance: "))

if ?? <= distance < 1200:
    input_distance = float(input("type distance (km): "))
if distance >= 1200 or (distance>=?? and input_distance>=1200):
    print("you can fly.")
else:
    print("you cant fly.")
'''

# part3
'''
def calculate_consumption(travel_distance, weather_modifier, plane_modifier):
    calc = travel_distance * weather_modifier * plane_modifier
    return calc

# 3.61 tonnes co2 per big plane 1 fly in 1000km
plane_modifier = 0,00361 per big plane, /2 per mid /4 smol plane
'''

print("           _")
print("         -=\`\ ")
print("     |\ ____\_\__")
print("   -=\c`******* *`) ")
print("      `~~~~~/ /~~`")
print("        -==/ /")
print("          '-'")
