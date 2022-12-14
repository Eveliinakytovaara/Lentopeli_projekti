import random

def chance_of_event():
    chance = random.randint(1, 15)
    print(chance)
    if chance == 1:
        "ticket check"
    elif chance == 2:
        "first class flight"
    elif chance == 3:
        "drink service"
    elif chance == 4:
        "turbulence"
    elif chance == 5:
        "emission free flight"
    else:
        return " "


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


def firstclass_ticket():
    print("You've found 100 euros under your seat! Congratulations! Your next flight will be first class")


def drink_service():
    answer = {
        "question" : { "text": "Would you like something to drink?",
        'drink' : '',
        'yes': 'yes',
        'no': 'no'
          },
        'blueberry_juice' : {
            'drink' : 'blueberry_juice',
        },
        'coffee' : {
            'drink' : 'coffee',
        },
        'coffee_with_milk' : {
            'drink' : 'coffee',
        },
        'coffee_with_sugar' : {
            'drink' : 'coffee',
        },
        'tea' : {
            'drink' : 'tea',
        }
    }
    return answer


def drink_question():
    answer = {
        "question": "Would you like something to drink?",
        'yes' : 'yes',
        'no' : 'no'
    }
    return answer


def emission_free_flight(consumption):
    print("You have won an emission free flight!")
    consumption = 0
    return consumption



