import random

def chance_of_event():
    chance = random.randint(1, 15)
    if chance == 1:
        return duty_free_shopping()
    elif chance == 2:
        return first_class_flight()
    elif chance == 3:
        return drink_service()
    elif chance == 4:
        return emission_free_flight()
    else:
        return ""

def first_class_flight():
    answer = {
        "question" : "Congratulations! You have found 100 euros under you seat "
                     "and your flight will be in first class! "
                     "Would you like a complimentary first class item?",
                        
        'url': 'Kuvat/ey-1.jpg',

        'options' : {

        'option1' : 'champange',

        'option2' : 'headphones',

        'option3' : 'neckpillow',

        'option4' : 'candies',

        'option5' : 'no, thank you'
        }
    }
    return answer


def duty_free_shopping():
    answer = {
        'question' : 'You have a long layover and have time to go duty free shopping! '
                     'Which item would you like to purchase?',
        
        'url' : 'Kuvat/dutyfree.jpg',

        'options' : {

            'option1' : 'chocolate',

            'option2' : 'perfume',

            'option3' : 'alcohol',

            'option4' : 'ugly souvenir',

            'option5' : 'make-up'
        }
    }
    return answer


def drink_service():
    answer = {
        "question": "Would you like something to drink?",

        'url' : 'Kuvat/flight-attendant-cart-drink-service-never-order.jpg',

        "options" : {

        'option1' : "blueberry juice",

        'option2' : 'coffee ',

        'option3' : 'coffee with milk',

        'option4' : 'coffee with sugar',

        'option5' : 'tea'
        }
    }
    return answer


def emission_free_flight():
    answer = {
        "question" : "Congratulations! You have won an emission free flight! The CO2 emissions from this flight "
                     "will not affect your score.",
        
        "url" : "Kuvat/emissionfree.jpg",

        "options" : {

        "option1" : "OK!"
        }
    }
    return answer



