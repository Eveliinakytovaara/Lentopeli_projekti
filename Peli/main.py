# kommentti

import mysql.connector

from Peli.main_game import flight_game


def open_database():
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='Nevermindme',
        autocommit=True)
    return connection


def check_if_int(value):
    if value.isdigit():
        return True
    return False


def print_main_menu():
    print("Tervetuloa lenopeliin!")
    print("1. Uusi peli")
    print("2. Jatka peliä")
    print("3. Katso ennätyksiä")
    print("4. Poistu pelistä")
    return


def main_menu():
    connection = open_database()
    print_main_menu()
    while True:
        choice = input("Valitse mitä haluat tehdä (1 - 4): ")
        if not check_if_int(choice):
            print("Virhe syöttö...")
            continue
        elif int(choice) == 1:
            screen_name = input("Syötä nimesi: ")
            # TODO pelaaja valitsee aloitus lentoaseman
            player_index = 0
            flight_game("", player_index, connection)
            print_main_menu()
        elif int(choice) == 2:
            screen_name = input("Syötä nimi: ")
            # TODO katso onko nimi tietokannassa ja onko peli kesken
        elif int(choice) == 3:
            # TODO tulosta kaikki valmiit pelit
            print("")
        else:
            print("Kiitos, että pelasit!")
            break


main_menu()
