from geopy import distance
def execute_sql(connection, sql):
    # print(f"execute: [{sql}]")
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
    return continent_name


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