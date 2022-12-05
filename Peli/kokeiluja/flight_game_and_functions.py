import mysql.connector
from geopy import distance


# MAIN FUNKTIOT

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


def end_screen(screen_name, co2_consumed, travel_distance, starting_location,
               s_planes_used, m_planes_used, l_planes_used):
    # TODO näytä vanhat tiedot
    screen_name
    print(f"Name: {screen_name}.")
    print(f"Consumed co2 {float(co2_consumed):.2f} ton.")
    print(f"Player {screen_name} travelled {travel_distance}km.")
    print(f"Player {screen_name} started game from {starting_location}.")
    print(f"Player {screen_name} used {s_planes_used} light planes.")
    print(f"Player {screen_name} used {m_planes_used} mid-size planes.")
    print(f"Player {screen_name} used {l_planes_used} Jumbo jets.")
    return


# MAIN GAME FUNKTIOT

# Suorittaa sql komennon
def execute_sql(connection, sql):
    print(f"execute: [{sql}]")
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    return values


# Hakee tietokannasta
def get_from_database(connection, column, table, where):
    sql = "SELECT " + column + " FROM " + table + " " + where
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
    if plane_type == "Light":
        plane = "s_planes_used"
    elif plane_type == "Mid-size":
        plane = "m_planes_used"
    else:
        plane = "l_planes_used"

    sql = "UPDATE player SET co2_consumed = co2_consumed + " + \
          str(co2_consumed) + ", travel_distance = travel_distance + " + str(travel_distance) + \
          ", " + plane + " = " + plane + " + 1, continents_visited = '" + str(continents_visited) + \
          "', location = '" + location + "', number_of_flights = number_of_flights + 1 WHERE id = " + str(player_index)
    execute_sql(connection, sql)
    return


# Laskee kulutuksen
def calculate_consumption(distance, weather_modifyer, plane_modifyer):
    calc = distance * weather_modifyer * plane_modifyer
    return calc


# Suorittaa pelaajan valinnan
def player_input(min_input, max_input):
    while True:
        choice = input(f"Choose({min_input} - {max_input} or 0 to quit to menu): ")
        if check_if_int(choice):
            if min_input <= int(choice) <= max_input:
                return int(choice) - 1
            elif int(choice) == 0:
                return -1
            else:
                print(f"Enter the number {min_input} - {max_input}")
        else:
            print("Incorrect input...")


# Hakee maanosan naapurit
def get_neighbouring_continents(_connection, current_airport):
    continent = get_from_database(_connection, "distinct continent", "airport",
                                  "where ident = '" + current_airport + "'")
    temp_neighbour = []
    for i in range(1, 5):
        temp = get_from_database(_connection, "neighbour_" + str(i), "neighbour", "where id = '" +
                                 str(continent[0]) + "'")
        temp_neighbour.append(temp[0])

    return temp_neighbour


# Hakee maanosan koko nimen maakoodin mukaan
def get_continent_name(_connection, continent):
    continent_name = get_from_database(_connection, "name", "neighbour", f"where id = '{continent}'")
    return continent_name[0]


# Hakee lentoasemia tai tietoa tietystä lentoasemasta, mutta palauttaa aina listan
def get_airport(_connection, airport_code, _type):
    temp_airport = get_from_database(_connection, _type, "airport", f"where ident = '{airport_code}'")
    return temp_airport[0]


# Hakee random lentokentän
def get_random_airports(_connection, continent_code, _type, count):
    is_continent = ''
    if continent_code != '':
        is_continent = f"and continent = '{continent_code}'"

    temp_airports = get_from_database(_connection, _type, "airport",
                                      f"where type != 'heliport' and type != 'closed' {is_continent}"
                                      f" ORDER BY RAND() LIMIT {count}")
    return temp_airports


# Hakee lentoaseman maan nimen ja palauttaa yhden str muutujan
def get_country(_connection, current_airport):
    country_name = get_from_database(_connection, "country.name", "country, airport",
                                     f"where airport.iso_country = country.iso_country and "
                                     f"airport.ident = '{current_airport}'")
    return country_name[0]


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
def get_random_weather(_connection, _type):
    weather = get_from_database(_connection, _type, "weather", "ORDER BY RAND() LIMIT 1")
    return weather[0]


# Hake sään tietokannasta
def get_weather(_connection, _type, weather):
    weather = get_from_database(_connection, _type, "weather", "where name = '" + weather + "'")
    return weather[0]


# Hakee lentokoneen koon matkan perusteella ja palauttaa tietoa siitä
def get_plane(_distance, _type):
    min_distance = 3000
    max_distance = 10000

    if _distance <= min_distance:
        if _type == "name":
            return "Light"
        else:
            return "0.75"
    elif max_distance > _distance > min_distance:
        if _type == "name":
            return "Mid-size"
        else:
            return "1"
    else:
        if _type == "name":
            return "Jumbo"
        else:
            return "1.5"


# Laskee lopullisen kulutuksen matkalta
def calculate_consumption(travel_distance, weather_modifier, plane_modifier):
    calc = (travel_distance * 0.0018) * weather_modifier * plane_modifier
    return calc


# FLIGHT GAME

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

        # Tulostetaan missä pelaaja on
        print(f"You are at {get_airport(connection, current_airport, 'name')}, "
              f"{get_country(connection, current_airport)}")

        # Haetaan naapuri maanosat listaan aloitus lentoaseman maanosan perusteella
        neighbours = get_neighbouring_continents(connection, current_airport)

        # Tulostetaan naapuri maanosat (for loop)
        print("Where would you like to fly next?")
        x = 0
        for i in neighbours:
            x += 1
            print(f"{x}: {get_continent_name(connection, i)}")

        # Pelaaja valitsee numerolla maanosan, mistä haetaan lentoasemia
        choice = player_input(0, len(neighbours))
        if choice == -1:
            break
        continent_choice = neighbours[int(choice)]

        # Luodaan lista, joka pitää sisällään kaiken tulostettavan datan lentoasemista
        airport_data = []
        # Luodaan erillinen tyhjä lista sään nimiä varten, joita ei tulosteta, jotta säätiloja voidaan hakea myöhemmin
        weather_name = []
        # Luodaan toinen lista, jossa on lentoasemien ident-koodeja (ei tulosteta vaan käytetään hakemiseen)
        airports = get_random_airports(connection, continent_choice, 'ident', 5)

        # Luodaan sisäänrakennettu lista (listoja lisan sisällä)
        for x in range(len(airports)):
            # Luodaan tilapäinen lista, joka sisältää ykittäisiä arvoja lentoasemasta
            # Tämä lista lisätään airport_data listan alkioksi
            temp = []
            # Haetaan lentoaseman nimi jo arvottujen lentoasemien koodien mukaan
            temp_airports = get_airport(connection, airports[x], 'name')
            temp.append(f"{'Airport:':11s}{temp_airports}")
            # Haetaan lentoaseman maan nimi
            temp.append(f"{'Country:':11s}{get_country(connection, airports[x])}")
            # Haetaan satunnainen säätilan nimi, mutta vain kuvaus lisätään tulostettaviin
            weather_name.append(get_random_weather(connection, "name"))
            temp.append(f"{'Weather:':11s}{get_weather(connection, 'description', weather_name[-1])}")
            # Lasketaan etäisyys
            temp_distance = get_distance(connection, current_airport, airports[x])
            # Lisätään etäisyys listaan string muutujana
            temp.append(f"{'Distance:':11s}{str(temp_distance)} km")
            # Haetaan lentokoneen koko nimenä etäisyyden perusteella
            temp.append(f"{'Plane:':11s}{get_plane(temp_distance, 'name')}")
            # Lisätään tilapäinen lista airport_data listaan
            airport_data.append(temp)

        # Tulostetaan listan airport_data arvot
        i = 0
        for x in range(len(airport_data)):
            i += 1
            print(f"{i}.")
            for o in airport_data[x]:
                print(o)

        # Pelaaja valisee lentoaseman minne, lentää listasta numerolla
        print("")
        print("Where would you like to fly?")
        choice = player_input(0, len(airport_data))
        if choice == -1:
            break

        # Haetaan arvot muuttujille, jotka vaikuttavat lennon kulutukseen
        travel_distance = get_distance(connection, current_airport, airports[choice])
        plane_modifier = float(get_plane(travel_distance, "mod"))
        weather_modifier = float(get_weather(connection, "modifier", weather_name[choice]))

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
            print("You have visited the following continents: ")
            for i in continents_visited:
                print(get_continent_name(connection, i))

        # Päivitetään uusi lentoasema
        current_airport = airports[choice]

    if len(continents_visited) >= 7:
        screen_name = get_from_database(connection, "screen_name", "player", f"where id = '{player_index}'")
        co2_consumed = get_from_database(connection, "co2_consumed", "player", f"where id = '{player_index}'")
        travel_distance = get_from_database(connection, "travel_distance", "player", f"where id = '{player_index}'")
        starting_location = get_from_database(connection, "starting_location", "player", f"where id = '{player_index}'")
        s_planes_used = get_from_database(connection, "s_planes_used", "player", f"where id = '{player_index}'")
        m_planes_used = get_from_database(connection, "m_planes_used", "player", f"where id = '{player_index}'")
        l_planes_used = get_from_database(connection, "l_planes_used", "player", f"where id = '{player_index}'")
        end_screen(screen_name[0], co2_consumed[0], travel_distance[0], starting_location[0],
                   s_planes_used[0], m_planes_used[0], l_planes_used[0])
