import geopy.distance
import mysql.connector
from geopy import distance


def open_database():
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='Nevermindme',
        autocommit=True)
    return connection


def get_from_database(connection):
    sql = ""
    kursori = connection.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos


connection = open_database()


def flight_game(starting_airport, sceen_name):
    # Tallenetaan aloitus lentokenttä muuttjaan (ident)
    current_airport = starting_airport
    while True:
        # Kaikki muutujat, joiden tietoja tallennetaan tietokantaan per lento
        co2_consumed = 0
        travel_distance = 0
        plane_modifier = 0

        # Hakee naapuri maanosat listaan aloitus lentoaseman maanosan perusteella
        neighbours = get_neighbour(current_airport)

        # Tulostetaan naapuri maanosat (for loop)
        print(neighbours)

        # Pelaaja valitsee numerolla maan osan
        choice = input("Valitse maanosa, minne lentää: ")
        continent_choice = neighbours[choice]

        # haetaan lentoasemia listaan valitusta maanosasta
        count = 5
        aiports = get_airports(continent_choice, count)

        # Tulostetaan valittavana olevat lentoasemat (for loop)
        print(aiports)
        weather_modifier = get_weather_modifier()

        choice = input("Valitse current_airport, minne lentää: ")
        airport_choice = airports[choice]

        travel_distance = get_distance(current_airport, airport_choice)
        plane_modifier = get_plane_modifier(travel_distance)
        # lennetään
        co2_consumed = calculate_consumption(distance, weather_modifier, plane_modifier)

        # Katsotaan onko kaikissa maanosissa käyty
        if get_from_database(continents_visited()) >= 7:
            break

        # Päivitetään tiedot keskeneräisenä tietokantaan
        update_database(sceen_name, co2_consumed, travel_distance)

    end_screen()
