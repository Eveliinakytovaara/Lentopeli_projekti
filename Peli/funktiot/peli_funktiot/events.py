from Peli.funktiot.main_menu_funktiot import *

def ticket_check(airport_data):
    check = input('Do you have a ticket? ')
    if check == 'Yes':
        print('Have a pleasant journey!')
    elif check == 'No':
        print('You cannot travel now! Go back to the airport and buy a ticket')
        print('Where would you like to fly?')
        i = 0
        for x in range(len(airport_data)):
            i += 1
            print(f"{i}.")
            for o in airport_data[x]:
                print(o)
        print("Where would you like to fly?")
        choice = player_input(0, len(airport_data))


def firstclass_ticket():
    print("You've found 100 euros under your seat! Congratulations! Your next flight will be first class")


def drink_service():
    choice = (input("Would you like a drink?"))
    choice_2 = ""
    choice_3 = ""
    if choice == "Yes":
        print("Would you like some blueberry juice, coffee or tea? ")
        if choice_2 == "blueberry juice":
            print("Here's some juice!")
        elif choice_2 == "coffee":
            print("Here's some coffee!")
            input("Would you like milk or sugar?")
            if choice_3 == "milk":
                print("Here's some milk!")
            elif choice_3 == "sugar":
                print("Here's some sugar!")
            else:
                print("Here's some of both!")
        elif choice_2 == "tea":
            print("Here's some tea!")
    elif choice_2 == "No":
        print("Ok, have a nice flight!")


def turbulence():
    print("Dear passengers, we are experiencing some turbulence, please remain seated and fasten your seatbelts.")
    # tähän väliin tärisemistä
    print("Dear passengers, we need to make an emergency landing to the closest airport")



