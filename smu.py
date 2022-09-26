import mysql.connector
from geopy import distance


def avaa_tietokanta():
    yhteys = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='Nevermindme',
        autocommit=True)
    return yhteys


yhteys = avaa_tietokanta()
