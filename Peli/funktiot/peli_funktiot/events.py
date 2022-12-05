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