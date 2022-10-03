# calculate_consumption(distance, weather_modifier, plane_modifier)
# Palauttaa lopullisen kulutuksen float arvona
# Parametrit ovat float (matka), float(sään kerroin), float (lentokoneen koon kerroin)

from geopy import distance
import mysql

def open_database():
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='root',
        autocommit=True)
    return connection


def calculate_consumption(distance, weather_modifyer, plane_modifyer)
    calc = distance * weather_modifyer * plane_modifyer
    return calc