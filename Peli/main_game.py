import random
from geopy import distance
from Peli.end_screen import end_screen


# Suorittaa sql komennon
def execute_sql(connection, sql):
    # print(f"execute: [{sql}]")
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    return values


# Hakee tietokannasta
def get_from_database(connection, column, table, where):
    sql = "SELECT " + " " + column + " FROM " + table + " " + where
    values = execute_sql(connection, sql)
    values = remove_pointless(values)
    return values


# Poistaa turhat merkit haku tuloksista
def remove_pointless(s):
    for i in range(len(s)):
        s[i] = str(s[i]).replace("'", "")
        s[i] = str(s[i]).replace("(", "")
        s[i] = str(s[i]).replace(")", "")
        s[i] = str(s[i]).replace(",", "")
        s[i] = str(s[i]).replace("]", "")
        s[i] = str(s[i]).replace("[", "")
    return s


# Katsoo, onko merkkijono int arvo
def check_if_int(value):
    if value.isdigit():
        return True
    return False


# Päivittää pelaajan tietoja tietokantaan
def update_player_data(connection, player_index, co2_consumed, travel_distance, plane_type, continents_visited,
                       location):
    if plane_type == "small plane":
        plane = "s_planes_used"
    elif plane_type == "medium plane":
        plane = "m_planes_used"
    else:
        plane = "l_planes_used"

    sql = "UPDATE player SET co2_consumed = co2_consumed + " + \
          str(co2_consumed) + ", travel_distance = travel_distance + " + str(travel_distance) + \
          ", " + plane + " = " + plane + " + 1, continents_visited = '" + str(continents_visited) + \
          "', location = '" + location + "', number_of_flights = number_of_flights + 1 WHERE id = " + str(player_index)
    execute_sql(connection, sql)
    return


# Suorittaa pelaajan valinnan
def player_input(min_input, max_input):
    while True:
        choice = input(f"Valitse({min_input} - {max_input}): ")
        if check_if_int(choice):
            if min_input <= int(choice) <= max_input:
                return int(choice) - 1
            else:
                print(f"syötä numero {min_input} - {max_input}")
        else:
            print("virhe syöttö...")


# Hakee maanosan naapurit
def get_neighbour(_connection, current_airport):
    continent = get_from_database(_connection, "distinct continent", "airport",
                                  "where ident = '" + current_airport + "'")
    temp_neighbour = []
    for i in range(1, 5):
        temp = get_from_database(_connection, "neighbour_" + str(i), "neighbour", "where id = '" +
                                 str(continent[0]) + "'")
        if temp[0] != "None":
            temp_neighbour.append(temp[0])

    return temp_neighbour


# Hakee lentoasemia tai tietoa tietystä lentoasemasta
def get_airports(_connection, continent, count, airport, _type):
    if _type == "name":
        data_type = "name"
    else:
        data_type = "ident"

    if airport == "":
        temp_airports = get_from_database(_connection, data_type, "airport", "where continent = '" +
                                          continent + "' ORDER BY RAND() LIMIT " + str(count))
        return temp_airports
    else:
        temp_airport = get_from_database(_connection, data_type, "airport", "where ident = '" + airport + "'")
        return temp_airport


# hakee tietokannasta lentoaseman koordinaatit
def calculate_distance(connection, airport_code):
    response = get_from_database(connection, "latitude_deg, longitude_deg", "airport",
                                 "where ident = '" + airport_code + "'")
    return response


# Laskee kahden lentoaseman välisen matkan kilometereinä
def get_distance(connection, current_airport, airport_choice):
    loc1 = calculate_distance(connection, current_airport)
    loc2 = calculate_distance(connection, airport_choice)
    gap = distance.distance(loc1, loc2).km
    return round(gap)


# Hakee satunnaisen säätilan tai tietoa tietystä säätilasta
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
        index = int(temp_indexes[0])
    values = get_from_database(_connection, data_type, "weather", "where id = '" + str(index) + "'")
    return values[0]


# Hakee lentokoneen koon matkan perusteella ja palauttaa tietoa siitä
def get_plane(_distance, _type):
    min_distance = 1200
    max_distance = 2500
    if _distance <= min_distance:
        if _type == "name":
            return "small plane"
        else:
            return "0.75"
    elif max_distance > _distance > min_distance:
        if _type == "name":
            return "medium plane"
        else:
            return "1.5"
    else:
        if _type == "name":
            return "big plane"
        else:
            return "2.0"


# Laskee lopullisen kulutuksen matkalta
def calculate_consumption(travel_distance, weather_modifier, plane_modifier):
    calc = travel_distance * weather_modifier * plane_modifier
    return calc


# Peli
def flight_game(starting_airport, player_index, connection):
    # Tallenetaan aloitus lentokenttä muuttjaan (ident-arvo)
    current_airport = starting_airport

    # Luodaan joukko, jolla pidetään muistissa maanosat, jossa pelaaja on käynyt
    # Joukkoihin ei tallennu kopoita, joten sen pituus on tarkka arvio, monessa maanosassa pelaaja on käynyt
    continents_visited = set()
    # Haetaan yhdessä string muutujassa mahdolliset edelliset maanosat, missä ollaan käyty
    continent_sql = get_from_database(connection, "continents_visited", "player",
                                      "where id = '" + str(player_index) + "'")

    # Lisätään string jaoteltuna 2 merkin pitusena joukkoon
    # esim. EUNAAS -> EU, NA, AS
    for i in range(0, len(continent_sql[0]), 2):
        continents_visited.add(continent_sql[0][i:i + 2])

    # Jos haku tuloksia ei löydy, niin joukkoon lisätään virheellisesti "None"
    # Poistetaan se
    continents_visited.discard("No")
    continents_visited.discard("ne")
    # Pelin loop
    while True:

        # Haetaan naapuri maanosat listaan aloitus lentoaseman maanosan perusteella
        neighbours = get_neighbour(connection, current_airport)

        # Tulostetaan naapuri maanosat (for loop)
        x = 0
        for i in neighbours:
            x += 1
            print(f"{x}: {i}")

        # Pelaaja valitsee numerolla maanosan, mistä haetaan lentoasemia
        print("Minne maanosaan haluat lentää?")
        print("")
        choice = player_input(1, len(neighbours))
        continent_choice = neighbours[int(choice)]

        # Luodaan lista, joka pitää sisällään kaiken tulostettavan datan lentoasemista
        airport_data = []
        # Luodaan erillinen tyhjä lista sään nimiä varten, joita ei tulosteta, jotta säätiloja voidaan hakea myöhemmin
        weather_name = []
        # Luodaan toinen lista, jossa on lentoasemien ident-koodeja (ei tulosteta vaan käyetään hakemiseen)
        airports = get_airports(connection, continent_choice, 5, "", "ident")

        # Luodaan sisäänrakennettu lista (listoja lisan sisällä)
        for x in range(len(airports)):
            # Luodaan tilapäinen lista, joka sisältää ykittäisiä arvoja lentoasemasta
            # Tämä lista lisätään listan alkioksi
            temp = []
            # Haetaan 1. pituinen lista lentoasemien nimiä
            temp_airports = get_airports(connection, "", 1, airports[x], "name")
            temp.append(temp_airports[0])
            # Haetaan satunnainen säätilan nimi ja sen kuvaus lisätään tulostettaviin
            weather_name.append(get_weather(connection, "name", ""))
            temp.append(get_weather(connection, "desc", weather_name[-1]))
            # Lasketaan etäisyys
            temp_distance = get_distance(connection, current_airport, airports[x])
            # Lisätään etäisyys listaan string muutujana
            temp.append(f"Travel distance: {temp_distance} km")
            # Haetaan lentokoneen koko nimenä etäisyyden perusteella
            temp.append(get_plane(temp_distance, "name"))
            # Lisätään tilapäinen lista airport_data listaan
            airport_data.append(temp)

        # Tulostetaan listan airport_data arvot
        i = 0
        for x in range(len(airport_data)):
            i += 1
            print(f"{i}.")
            for o in airport_data[x]:
                print(o)
            print("")

        # Pelaaja valisee lentoaseman minne, lentää listasta numerolla
        print("Minne haluat lentää?")
        choice = player_input(1, len(airport_data))

        # Haetaan arvot muuttujille, jotka vaikuttavat lennon kulutukseen
        travel_distance = get_distance(connection, current_airport, airports[choice])
        plane_modifier = float(get_plane(travel_distance, "mod"))
        weather_modifier = float(get_weather(connection, "mod", weather_name[choice]))

        # Lasketaan lopullinen kulutus
        co2_consumed = calculate_consumption(travel_distance, weather_modifier, plane_modifier)

        # Lisätään maanosa, jonne lennettiin, joukkoon (Joukoissa ei voi olla kopioita)
        current_continent = get_from_database(connection, "continent", "airport",
                                              "WHERE ident = '" + airports[choice] + "'")
        continents_visited.add(current_continent[0])

        # Tietokantaan ei voi lisätä listoja, joten tehdään listan arvoista string muuttuja
        # esim. on käynyt EU ja NA -> EUNA
        continent_str = ""
        for i in continents_visited:
            continent_str += i

        # Päivitetään tiedot tietokantaan
        update_player_data(connection, player_index, co2_consumed, travel_distance,
                           get_plane(travel_distance, "name"), continent_str, airports[choice])

        # Katsotaan onko kaikissa maanosissa käyty
        if len(continents_visited) >= 7:
            break
        else:
            # jos ei, jatketaan peliä ilmoittamalla, että missä on käynyt
            print("Olet käynyt seuraavissa maanosissa: ")
            for i in continents_visited:
                print(i)

        # Päivitetään uusi lentoasema
        current_airport = airports[choice]

    end_screen()
