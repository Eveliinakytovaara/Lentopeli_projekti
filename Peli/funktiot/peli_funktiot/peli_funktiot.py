from geopy import distance
import mysql.connector
import requests


def open_database():
    _connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='root',
        autocommit=True
    )
    return _connection


def execute_sql(sql):
    # print(f"execute: [{sql}]")
    connection = open_database()
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    return values


# Hakee tietokannasta
def get_from_database(column, table, where):
    sql = "SELECT " + column + " FROM " + table + " " + where
    values = execute_sql(sql)
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


def create_player(screen_name, starting_airport):
    sql = "Insert Into player (screen_name, co2_consumed, travel_distance, location, starting_location, " \
          "number_of_flights, s_planes_used, m_planes_used, l_planes_used, continents_visited)"

    starting_continent = get_from_database('continent', 'airport', f'where ident = "{starting_airport}"')

    sqll = f" VALUES ('{screen_name}', 0, 0, '{starting_airport}', '{starting_airport}', 0, 0, 0, 0, " \
           f"'{starting_continent[0]}');"
    execute_sql(sql + sqll)
    last_player_id = execute_sql('SELECT max(id) FROM player')
    return last_player_id


def clear_player_data():
    sql = "delete from player"
    sqql = "ALTER TABLE player AUTO_INCREMENT = 1"
    execute_sql(sql)
    execute_sql(sqql)
    return


# Päivittää pelaajan tietoja tietokantaan
def update_player_data(player_index, co2_consumed, travel_distance, plane_type, continents_visited,
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
    execute_sql(sql)
    return


def update_player(id, column, value):
    sql = f'update player set {column} = "{value}" where id = "{id}"'
    execute_sql(sql)
    return


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
def get_neighbouring_continents(current_airport):
    continent = get_from_database("distinct continent", "airport",
                                  "where ident = '" + current_airport + "'")
    temp_neighbour = []
    for i in range(1, 5):
        temp = get_from_database("neighbour_" + str(i), "neighbour", "where id = '" +
                                 str(continent[0]) + "'")
        temp_neighbour.append(temp[0])

    return temp_neighbour


# Hakee maanosan koko nimen maakoodin mukaan
def get_continent_name(continent):
    continent_name = get_from_database("name", "neighbour", f"where id = '{continent}'")
    if len(continent_name) > 0:
        return continent_name[0]
    else:
        return ""


def compare_continents(continent, player_id):
    continents_visited = set()
    continent_sql = get_from_database("continents_visited", "player",
                                      f"where id = '{player_id}'")
    for i in range(0, len(continent_sql[0]), 2):
        continents_visited.add(continent_sql[0][i:i + 2])
    continents_visited.discard("No")
    continents_visited.discard("ne")
    continents_visited.add(continent)

    continent_str = ""
    for i in continents_visited:
        continent_str += i

    return continent_str


# Hakee lentoasemia tai tietoa tietystä lentoasemasta, mutta palauttaa aina listan
def get_airport(airport_code, _type):
    temp_airport = get_from_database(_type, "airport", f"where ident = '{airport_code}'")
    return temp_airport[0]


# Hakee random lentokentän
def get_random_airports(continent_code, _type, count):
    is_continent = ''
    if continent_code != '':
        is_continent = f"and continent = '{continent_code}'"

    temp_airports = get_from_database(_type, "airport",
                                      f"where type != 'heliport' and type != 'closed' {is_continent}"
                                      f" ORDER BY RAND() LIMIT {count}")
    return temp_airports


def get_weather(airport_code):
    lat = get_from_database("latitude_deg", "airport", f"where ident='{airport_code}'")[0]
    lon = get_from_database("longitude_deg", "airport", f"where ident='{airport_code}'")[0]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=c9dca395b68f0f13b3cb7f4eedc59865"
    response = requests.get(url)
    data = response.json()
    name = data['weather'][0]['main']
    modifier = get_from_database("modifier", "weather", f"where name='{name}'")[0]
    result = name, modifier
    return result


# Hakee lentoaseman maan nimen ja palauttaa yhden str muutujan
def get_country(current_airport):
    country_name = get_from_database("country.name", "country, airport",
                                     f"where airport.iso_country = country.iso_country and "
                                     f"airport.ident = '{current_airport}'")
    return country_name[0]


# hakee tietokannasta lentoaseman koordinaatit
def calculate_distance(airport_code):
    response = get_from_database("latitude_deg, longitude_deg", "airport",
                                 "where ident = '" + airport_code + "'")
    return response


# Laskee kahden lentoaseman välisen matkan kilometereinä
def get_distance(current_airport, airport_choice):
    loc1 = calculate_distance(current_airport)
    loc2 = calculate_distance(airport_choice)
    gap = distance.distance(loc1, loc2).km
    return round(gap)


def get_plane(_distance, _type):
    plane_class = get_from_database(_type, "planes",
                                    f"where min_distance < {str(_distance)} and max_distance >= {str(_distance)}")

    return plane_class[0]


"""
# Hakee lentokoneen koon matkan perusteella ja palauttaa tietoa siitä
def get_plane(_distance, _type):
    min_distance = 0
    mid_distance = 3300
    max_distance = 9500

    if _distance <= min_distance:
        if _type == "name":
            return "Light"
        else:
            return "1.13"
    elif max_distance > mid_distance > _distance > min_distance:
        if _type == "name":
            return "Mid-size"
        else:
            return "3.7"
    else:
        if _type == "name":
            return "Jumbo"
        else:
            return "10.4"
"""  # old function


# Laskee lopullisen kulutuksen matkalta
# 0.79 on kerroin litroista kilogrammaan
# 2.3 kerroin on co2 per 1 kilo poltoainesta

def calculate_consumption(travel_distance, weather_modifier, plane_modifier):
    calc = (((travel_distance * plane_modifier) * weather_modifier) * 0.79) * 2.3
    return calc
