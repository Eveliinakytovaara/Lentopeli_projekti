for luku in range
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


def calculate_distance(connection, airport_code):
    sql1 = 'select latitude_deg, longitude_deg from airport where ident = "' + airport_code + '"'
    cursor = connection.cursor()
    cursor.execute(sql1)
    response = cursor.fetchall()
    return response


def get_distance(connection, current_airport, airport_choice):
    loc1 = calculate_distance(connection, current_airport)
    loc2 = calculate_distance(connection, airport_choice)
    gap = distance.distance(loc1, loc2).km
    return gap


connection = open_database()
distance = get_distance(connection, "EFHK", "OMAF")
print(f"Distance between airports is {distance:.3f} km")