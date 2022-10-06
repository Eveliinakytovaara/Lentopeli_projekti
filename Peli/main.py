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
    print("Welcome to the flight game!")
    print("1. New game")
    print("2. Continue the game")
    print("3. Show the records")
    print("4. Finish the game")
    return


def create_player(connection, screen_name, starting_airport):
    sql = "Insert Into player (screen_name, co2_consumed, travel_distance, location, starting_location, " \
          "number_of_flights, s_planes_used, m_planes_used, l_planes_used, continents_visited)"

    starting_continent = get_from_database(connection, 'continent', 'airport', f'where ident = "{starting_airport}"')

    sqll = f" VALUES ('{screen_name}', 0, 0, '{starting_airport}', '{starting_airport}', 0, 0, 0, 0, " \
           f"'{starting_continent[0]}');"
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
        choice = input("Choose what you want to do (1 - 4): ")
        if not check_if_int(choice):
            print("Incorrect input...")
            continue
        elif int(choice) == 1:
            screen_name = input("Enter your name: ")

            # print("Where would you like to start the game?")
            # airports = get_airports(connection, "", 5, "name", "")
            # for i in airports:
            #     print("")
            #     print(i)
            # while not check_if_int(choice):
            #     choice = input(f"1 - {len(airports)}: ")

            create_player(connection, screen_name, "EFHK")

            player_index = get_from_database(connection, "max(id)", "player", "")
            player_index = int(player_index[0])
            print("")
            flight_game("EFHK", player_index, connection)
            print_main_menu()
        elif int(choice) == 2:
            print("")
            print("Incomplete games:")
            incomplete_games = get_from_database(connection, "id, screen_name, location", "player",
                                                 "where CHAR_LENGTH(continents_visited) < 14")

            for i in incomplete_games:
                split_list = i.split()
                index = 0
                for obj in split_list:
                    index += 1
                    printed_string = ""
                    if index == 2:
                        printed_string = "Name: "
                    elif index == 3:
                        printed_string = "Current location: "
                    print(printed_string + obj)
                print("")

            print("")
            input("")
        else:
            print("Thank you for playing!")
            break


main_menu()
