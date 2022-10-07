import mysql.connector

from Peli.main_game import flight_game, execute_sql, get_from_database, check_if_int, player_input, get_airports, get_country


def open_database():
    _connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='root',
        autocommit=True)
    return _connection


def print_main_menu():
    print("")
    print("Welcome to the flight game!")
    print("1. New game")
    print("2. Continue the game")
    print("3. How to play?")
    print("4. Show the high score")
    print("5. Exit")
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


def show_games(games, _connection):
    if len(games) > 0:
        for i in games:
            split_list = i.split()
            index = 0
            for obj in split_list:
                index += 1
                printed_string = ""
                if index == 1:
                    print(index)
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
    else:
        print("No data found...")
    return


def main_menu():
    connection = open_database()
    print_main_menu()
    while True:
        choice = input("Choose what you want to do (1 - 5): ")
        print("")
        if not check_if_int(choice):
            print("Incorrect input...")
            continue
        elif int(choice) == 1:
            screen_name = input("Enter your name: ")
            airports_codes = get_airports(connection, "EU", 5, "", "ident")
            print("")
            print("Where would you like to start the game?")
            for i in range(len(airports_codes)):
                print("")
                print(f"{i + 1}.  {get_airports(connection, 'EU', 1, airports_codes[i], 'name')[0]}, {get_country(connection, airports_codes[i])}")
            print("")
            choice = player_input(1, len(airports_codes))
            if choice == -1:
                print_main_menu()
                continue
            starting_airport = airports_codes[choice]
            create_player(connection, screen_name, starting_airport)

            player_index = get_from_database(connection, "max(id)", "player", "")
            player_index = int(player_index[0])
            print("")
            flight_game(starting_airport, player_index, connection)
            print_main_menu()
        elif int(choice) == 2:
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
                    print_main_menu()
                else:
                    print("Exiting")
                    continue
        elif int(choice) == 3:
            print("Welcome to flight game!")
            print("Your objective is to visit every continent.")
            print("The lower your co2 consumption is the higher you place on the leaderboards!")
            print("Pay attention to the flight distance, weather and plane you have for flights.")
            print("They affect your co2 consumption!")
            print("Good luck sucker!")
            input("Press enter to become a gamer...")
            print_main_menu()
        elif int(choice) == 4:
            complete_games = get_from_database(connection, "id, screen_name, location, co2_consumed,travel_distance, "
                                                           "number_of_flights, s_planes_used, m_planes_used,"
                                                           " l_planes_used"
                                               , "player",
                                               "where CHAR_LENGTH(continents_visited) >= 14 "
                                               "ORDER BY co2_consumed")

            show_games(complete_games, connection)
            if len(complete_games) > 0:
                print("Do you wish to reset all save data?")
                while True:
                    choice = input("y/n? ")
                    if choice == "y":
                        clear_player_data(connection)
                        print("Data reset...")
                        break
                    else:
                        break
                print_main_menu()
        elif int(choice) == 5:
            print("Thank you for playing!")
            break
        else:
            print("Wrong number dummy!")


main_menu()
