# get_distance(connection, current_airport, airport_choice)
# Palauttaa float arvon, joka on kahden lentoaseman välinen matka
# Molemmat parametrit ovat string muuttujia (lentoasemien ident-koodi)

import mysql.connector
from geopy import distance
from Peli.main_game import flight_game

def open_database():
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='root',
        autocommit=True)
    return connection


def get_distance(connection, airport_code):

    sql1 = 'select latitude_deg, longitude_deg from airport where ident = "' + airport_code + '"'
    cursor = connection.cursor()
    cursor.execute(sql1)
    response = cursor.fetchall()
    return response

current_airport = input("Enter your current airport, please: ")
airport = input("Enter your next destination, please: ")
connection = open_database()
loc1= get_distance(connection, current_airport)
loc2 = get_distance(connection, airport)
gap = distance.distance(loc1, loc2).km

print(f"Distance between {current_airport} and {airport} is {gap:.3f} km")
