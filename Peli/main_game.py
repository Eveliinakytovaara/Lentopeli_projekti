from random import random
from geopy import distance
from Peli.end_screen import end_screen


def execute_sql(connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    return values


def get_from_database(connection, column, table, where):
    sql = "SELECT " + " " + column + " FROM " + table + " " + where
    values = execute_sql(connection, sql)
    return values


def remove_pointless(s):
    for i in range(len(s)):
        s[i] = str(s[i]).replace("'", "")
        s[i] = str(s[i]).replace("(", "")
        s[i] = str(s[i]).replace(")", "")
        s[i] = str(s[i]).replace(",", "")
    return s


def update_player_data(connection, player_index, co2_consumed, travel_distance, plane_type, continents_visited):
    if plane_type == "small plane":
        plane = "s_planes_used"
    elif plane_type == "medium plane":
        plane = "m_planes_used"
    else:
        plane = "l_planes_used"

    sql = "UPDATE player SET co2_consumed = co2_consumed + " + \
          str(co2_consumed) + ", travel_distance = travel_distance + " + str(travel_distance) + \
          ", " + plane + " = " + plane + " + 1, continents_visited = " + str(continents_visited) + \
          " WHERE id = " + str(player_index)
    execute_sql(connection, sql)
    return


def calculate_distance(connection, airport_code):
    sql = get_from_database(connection, "latitude_deg, longitude_deg", "airport", "where ident '" + airport_code + "'")
    response = execute_sql(connection, sql)
    return response


def get_distance(connection, current_airport, airport_choice):
    loc1 = calculate_distance(connection, current_airport)
    loc2 = calculate_distance(connection, airport_choice)
    gap = distance.distance(loc1, loc2).km
    return gap


def get_weather(_connection, _type, weather_name):
    if _type == "name":
        data_type = "name"
    elif _type == "mod":
        data_type = "modifier"
    else:
        data_type = "description"

    if weather_name == "":
        index = random.randint(1, 11)
    else:
        temp_indexes = get_from_database(_connection, "id",
                                         "weather", "where name = '" + weather_name + "'")
        temp_indexes = remove_pointless(temp_indexes)
        index = int(temp_indexes[0])
    values = get_from_database(_connection, data_type, "weather", "where id = '" + str(index) + "'")
    values = remove_pointless(values)
    return values[0]


def calculate_consumption(travel_distance, weather_modifier, plane_modifier):
    calc = travel_distance * weather_modifier * plane_modifier
    return calc


def flight_game(starting_airport, player_index, connection):
    # Tallenetaan aloitus lentokenttä muuttjaan (ident)
    current_airport = starting_airport
    # Luodaan joukko, jolla pidetään muistissa maanosat, jossa pelaaja on käynyt
    continents_visited = set()
    while True:

        # Haetaan naapuri maanosat listaan aloitus lentoaseman maanosan perusteella
        neighbours = get_neighbour(connection, current_airport)

        # Tulostetaan naapuri maanosat (for loop)
        def get_neighbour(connection, current_airport):
            neighbours = set(get_from_database(connection, "continent", "airport", "where not ident '" + current_airport + "'"))
            for x in neighbours:
            print(x)
            return
  
        # Pelaaja valitsee numerolla maanosan, mistä haetaan lentoasemia
        choice = input("Valitse maanosa, minne lentää (1 - X): ")
        continent_choice = neighbours[choice]

        # Haetaan lentoasemien indet-koodeja listaan valitusta maanosasta
        airports = get_airports(connection, continent_choice, 5, "ident", "")
        def get_airports(connection, continent, count, airport, type):
            list_of_airports = set(get_from_database(connection, "name", "type", "airport", "where continent '" + continent_choice + "'"))
            for a in list_of_airports[0:5]:
               print(a)
               return
        # Luodaan muuttuja for loopin ulkopuolelle, jotta muistetaan käytettävä säätila
        weather_name = ""
        # Luodaan lista, joka pitää sisällään kaiken tulostettavan datan lentoasemista
        airport_data = []
        for i in range(len(airports)):
            # Luodaan tilapäinen lista, joka sisältää ykittäisiä arvoja lentoasemasta
            temp = []
            # Haetaan lentoaseman nimi
            temp.append(get_airports(connection, "", 1, "name", airports[i]))
            # Haetaan satunnainen säätilan nimi
            weather_name = get_weather(connection, "name", "")
            temp.append(get_weather(connection, "desc", weather_name))
            # Lasketaan etäisyys
            temp_distance = get_distance(connection, current_airport, airports[i])
            # Lisätään etäisyys listaan
            temp.append(str(temp_distance))
            # Haetaan lentokoneen koko nimenä etäisyyden perusteella
            temp.append(get_plane(temp_distance, "size"))
            # Lisätään tilapäinen lista airport_data listaan
            airport_data.append(temp)

        # Tulostetaan listan arvot
        for i in range(len(airport_data)):
            for o in airport_data[i]:
                print(o)
            print("")

        # Pelaaja valisee lentoaseman minne, lentää listasta numerolla
        choice = input("Valitse current_airport, minne lentää (1 - X): ")

        # Haetaan arvot muuttujille, jotka vaikuttavat lennon kulutukseen
        travel_distance = get_distance(connection, current_airport, airports[choice])
        plane_modifier = float(get_plane(travel_distance, "mod"))
        weather_modifier = float(get_weather(connection, "mod", weather_name))

        # Lasketaan lopullinen kulutus
        co2_consumed = calculate_consumption(travel_distance, weather_modifier, plane_modifier)

        # Lisätään maanosa, jonne lennettiin, joukkoon (kopioita ei lisätä)
        current_continent = get_from_database(connection, "continent", "airport",
                                              "WHERE ident = " + current_airport)
        continents_visited.add(current_continent[0])

        # Päivitetään tiedot tietokantaan
        update_player_data(player_index, co2_consumed, travel_distance, len(continents_visited))
        # Päivitetään nykyinen lentoasema
        current_airport = airports[choice]

        # Katsotaan onko kaikissa maanosissa käyty
        if len(continents_visited) >= 7:
            break

    end_screen()
