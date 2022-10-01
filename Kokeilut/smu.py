import mysql.connector

from Peli.main_game import flight_game


def check_if_int(value):
    if value.isdigit():
        return True
    return False


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
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    return values


def main_menu():
    connection = open_database()
    print("Tervetuloa lenopeliin!")
    print("1. Uusi peli")
    print("2. Jatka peliä")
    print("3. Katso ennätyksiä")
    print("4. Poistu pelistä")

    while True:
        choice = input("Valitse mitä haluat tehdä (1 - 3): ")
        if not check_if_int(choice):
            print("Virhe syöttö...")
            continue
        elif int(choice) == 1:
            screen_name = input("Syötä nimesi: ")
            # TODO pelaaja valitsee aloitus lentoaseman

            flight_game("", screen_name)


main_menu()
