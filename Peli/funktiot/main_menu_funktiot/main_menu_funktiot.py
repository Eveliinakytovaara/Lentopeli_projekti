import mysql.connector
from Peli.funktiot.main_menu_funktiot.main_game_program import *


def open_database():
    _connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='Nevermindme',
        autocommit=True)
    return _connection


def create_player(connection, screen_name, starting_airport):
    sql = "Insert Into player (screen_name, co2_consumed, travel_distance, location, starting_location, " \
          "number_of_flights, s_planes_used, m_planes_used, l_planes_used, continents_visited)"

    starting_continent = get_from_database(connection, 'continent', 'airport', f'where ident = "{starting_airport}"')

    sqll = f" VALUES ('{screen_name}', 0, 0, '{starting_airport}', '{starting_airport}', 0, 0, 0, 0, " \
           f"'{starting_continent[0]}');"
    execute_sql(connection, sql + sqll)
    return


def clear_player_data(_connection):
    sql = "delete from player"
    sqql = "ALTER TABLE player AUTO_INCREMENT = 1"
    execute_sql(_connection, sql)
    execute_sql(_connection, sqql)
    return


def start_a_new_game(connection):
    screen_name = input("Enter your name: ")
    airports_codes = get_random_airports(connection, '', 'ident', 5)
    print("")
    print("Where do you want to start a game?")
    for i in range(len(airports_codes)):
        print("")
        print(
            f"{i + 1}.  {get_airport(connection, airports_codes[i], 'name')}, {get_country(connection, airports_codes[i])}")
    print("")
    choice = player_input(1, len(airports_codes))
    if choice == -1:
        return
    starting_airport = airports_codes[choice]
    create_player(connection, screen_name, starting_airport)

    player_index = get_from_database(connection, "max(id)", "player", "")
    player_index = int(player_index[0])
    print("")
    flight_game(starting_airport, player_index, connection)
    return


def continue_the_game(connection):
    incomplete_games = get_from_database(connection, "id, screen_name, location", "player",
                                         "where CHAR_LENGTH(continents_visited) < 14")
    show_games(incomplete_games, connection)
    if len(incomplete_games) > 0:
        print(f"Choose a file to continue (0 to cancel)")
        choice = player_input(0, len(incomplete_games))
        if choice + 1 >= 1:
            player_airport = get_from_database(connection, "location", "player",
                                               f"where id = {incomplete_games[choice][0]}")
            flight_game(player_airport[0], choice + 1, connection)
        else:
            print("Exiting")
            return


def show_the_rules():
    print("Welcome to the flight game!")
    print("The goal is to visit every continent.")
    print("The lower your co2 consumption is the higher your place is on the leaderboards!")
    print("Pay attention to the flight distance, weather and plane you choose for flights.")
    print("They affect your co2 consumption!")
    input("Press enter to start your journey...")
    return


def show_the_high_score(connection):
    complete_games = get_from_database(connection, "id, screen_name, location, co2_consumed,travel_distance, "
                                                   "number_of_flights, s_planes_used, m_planes_used,"
                                                   " l_planes_used"
                                       , "player",
                                       "where CHAR_LENGTH(continents_visited) >= 14 "
                                       "ORDER BY co2_consumed ASC")

    show_games(complete_games, connection)
    if len(complete_games) > 0:
        print("Do you want to reset all saved data?")
        while True:
            choice = input("y/n? ")
            if choice == "y":
                clear_player_data(connection)
                print("Data reset...")
                break
            else:
                break
        return


def show_games(games, _connection):
    if len(games) > 0:
        number = 1
        for i in games:
            split_list = i.split()
            index = 0
            for obj in split_list:
                index += 1
                printed_string = ""
                if index == 1:
                    print(number)
                    continue
                elif index == 2:
                    printed_string = "Name: "
                elif index == 3:
                    printed_string = "Latest location: "
                    obj = get_from_database(_connection, "name", "airport", f"where ident = '{obj}'")[0]
                elif index == 4:
                    printed_string = "Co2 consumed: "
                    obj += "tons"
                elif index == 5:
                    printed_string = "Travel distance: "
                    obj += "km"
                elif index == 6:
                    printed_string = "Number of flights: "
                elif index == 7:
                    printed_string = "Light planes used: "
                elif index == 8:
                    printed_string = "Mid-size planes used:"
                elif index == 9:
                    printed_string = "Jumbo jets used: "
                print(printed_string + obj)

            print("")
            number += 1
    else:
        print("No data found...")
    return
