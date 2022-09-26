import mysql.connector
from geopy import distance


def open_database():
    yhteys = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='Nevermindme',
        autocommit=True)
    return yhteys


def get_from_database():
    sql = ""
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos


yhteys = open_database()


def flight_game(starting_airport, sceen_name):
    #Tallenetaan aloitus lentokenttä muuttjaan
    lentoasema = starting_airport
    while True:
        #Hakee naapuri maanosat listaan aloitus lentoaseman maanosan perusteella
        neighbours = get_neighbour(starting_airport)

        #Tulostetaan naapuri maanosat (for loop)
        print(neighbours)

        #Pelaaja valitsee numerolla maan osan
        choice = input("Valitse maanosa, minne lentää: ")

        #haetaan lentoasemia listaan valitusta maanosasta
        count = 5
        aiports = get_airports(choice, count)

        #Tulostetaan valittavana olevat lentoasemat (for loop)
        print(aiports)
        weather_modifier = get_weather_modifier()

        choice = input("Valitse lentoasema, minne lentää: ")

        plane_modifier = get_distance(starting_airport, get_airport(choice))
        #lennetään
        calculate_consumption(distance, weather_modifier, plane_modifier)

        #Katsotaan onko kaikissa maanosissa käyty
        if get_from_database(continents_visited()) >= 7:
            break

        #Päivitetään tiedot keskeneräisenä tietokantaan
        update_database(sceen_name)

    end_screen()

