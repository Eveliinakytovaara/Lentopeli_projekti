from Peli.main_game import check_if_int

from Peli.funktiot.main_funktiot import open_database, start_a_new_game, continue_the_game, \
    show_the_rules, show_the_high_score


def main_menu():
    connection = open_database()
    while True:
        choice = input("Choose what you want to do (1 - 5): ")
        print("")
        if not check_if_int(choice):
            print("Incorrect input...")
            continue
        elif int(choice) == 1:
            start_a_new_game(connection)
        elif int(choice) == 2:
            continue_the_game(connection)
        elif int(choice) == 3:
            show_the_rules()
        elif int(choice) == 4:
            show_the_high_score(connection)
        elif int(choice) == 5:
            print("Thank you for playing!")
            break
        else:
            print("Wrong number dummy!")


main_menu()
