import mysql.connector

from Peli.main_game import flight_game, execute_sql, get_from_database, check_if_int


def open_database():
    _connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='Nevermindme',
        autocommit=True)
    return _connection


def print_main_menu():
    print("")
    print("Tervetuloa lenopeliin!")
    print("1. Uusi peli")
    print("2. Jatka peliä")
    print("3. Katso ennätyksiä")
    print("4. Poistu pelistä")
    return


def create_player(connection, screen_name, starting_airport):
    sql = "Insert Into player (screen_name, co2_consumed, travel_distance, location, strating_location, " \
          "number_of_flights, s_planes_used, m_planes_used, l_planes_used, continents_visited)"
    sqll = " VALUES ('" + screen_name + "', 0, 0, '" + starting_airport + "', '" + starting_airport +\
           "', 0, 0, 0, 0, null);"
    execute_sql(connection, sql + sqll)
    return


def clear_player_data(_connection):
    sql = "delete from player; ALTER TABLE player AUTO_INCREMENT = 1;"
    execute_sql(_connection, sql)
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

            # print("Mistä haluat aloittaa lentopelin?")
            # airports = get_airports(connection, "", 5, "name", "")
            # for i in airports:
            #     print("")
            #     print(i)
            # while not check_if_int(choice):
            #     choice = input(f"1 - {len(airports)}: ")

            create_player(connection, screen_name, "EFHK")

            player_index = get_from_database(connection, "max(id)", "player", "")
            player_index = int(player_index[0])

            flight_game("EFHK", player_index, connection)
            print_main_menu()
        elif int(choice) == 2:
            print("")
        elif int(choice) == 3:
            print(get_from_database(connection, "*", "player", "where continents_visited = 7"))
            print("")
            while True:
                yes_no = input("Haluatko tyhjentää ennätykset (y/n)? ")
                if yes_no == "y":
                    clear_player_data(connection)
                elif yes_no == "n":
                    break
                else:
                    print("virhe syöttö...")
            print_main_menu()
        else:
            print("Kiitos, että pelasit!")
            break


main_menu()
