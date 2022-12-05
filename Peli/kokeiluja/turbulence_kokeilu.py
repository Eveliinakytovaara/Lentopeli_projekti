from Peli.funktiot.peli_funktiot import *
from Peli.funktiot.main_menu_funktiot import *

# Pelaaja valisee lentoaseman minne, lentää listasta numerolla
print("")
print("Where would you like to fly?")
choice = player_input(0, len(airport_data))
if choice == -1:
    break

def miumau():
    nyt_tarisee = travel_distance / 2

def get_closest_airport(_connection, current_airport):
    airport = get_from_database(_connection, "latitude_deg, longitude_deg", "airport",
                                f"where ident = '{current_airport}'")


# Haetaan arvot muuttujille, jotka vaikuttavat lennon kulutukseen
travel_distance = get_distance(connection, current_airport, airports[choice])
plane_modifier = float(get_plane(travel_distance, "mod"))
weather_modifier = float(get_weather(connection, "modifier", weather_name[choice]))

def get_random_airports(_connection, continent_code, _type, count):
    is_continent = ''
    if continent_code != '':
        is_continent = f"and continent = '{continent_code}'"


def get_neighbouring_continents(_connection, current_airport):
    continent = get_from_database(_connection, "distinct continent", "airport",
                                  "where ident = '" + current_airport + "'")
    temp_neighbour = []
    for i in range(1, 5):
        temp = get_from_database(_connection, "neighbour_" + str(i), "neighbour", "where id = '" +
                                 str(continent[0]) + "'")
        temp_neighbour.append(temp[0])

    return temp_neighbour