import geopy.distance
from geopy import distance


def get_from_database(connection, column, table, where):
    sql = "SELECT " + column + " FROM " + table + " " + where
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    return values


def update_player_data(player_index, co2_consumed, travel_distance, plane_type, continent):
    plane = ""
    if plane_type == "small plane":
        plane = "s_planes_used"
    elif plane_type == "medium plane":
        plane = "m_planes_used"
    else:
        plane = "l_planes_used"

    sql = "UPDATE player SET co2_consumed = co2_consumed + " + \
          co2_consumed + ", travel_distance = travel_distance + " + travel_distance + \
          ", " + plane + " = " + plane + " + 1, "
    print(sql)
    return


def flight_game(starting_airport, player_index, connection):
    # Tallenetaan aloitus lentokenttä muuttjaan (ident)
    current_airport = starting_airport
    while True:
        # Kaikki muutujat, joiden tietoja tallennetaan tietokantaan per lento
        co2_consumed = 0
        travel_distance = 0
        plane_modifier = 0

        # Haetaan naapuri maanosat listaan aloitus lentoaseman maanosan perusteella
        # TODO neighbours = get_neighbour(current_airport)

        # Tulostetaan naapuri maanosat (for loop)
        # TODO

        # Pelaaja valitsee numerolla maanosan, mistä haetaan lentoasemia
        choice = input("Valitse maanosa, minne lentää (1 - X): ")
        # TODO continent_choice = neighbours[choice]

        # Haetaan lentoasemia listaan valitusta maanosasta
        # TODO airports = get_airports(continent_choice, count)
        # Haetaan yhtä iso lista säätilojen nimiä, mutta tulostetaan kuvauksia (for loop)
        # TODO weathers.append(get_weather("name", ""))
        # Haetaan yhtä iso lista matkan pituusksia (for loop)
        # TODO distances.append(get_distance(current_airport, airports[i]))
        # Haetaan yhtä iso lista koneen kokoja matkojen perusteella
        # TODO planes.append(get_plane(current_airport, airports[i]))

        # Tulostetaan tieto kaikista listoista (for loop)
        # TODO print()

        # Pelaaja valisee lentoaseman minne, lentää listasta numerolla
        # Tallennetaan muutujiin tieto kaikista ylläolevista listoista
        choice = input("Valitse current_airport, minne lentää (1 - X): ")
        # TODO airport_choice = airports[choice]
        # TODO weather = weathers[choice]
        # TODO distance = distances[choice]
        # TODO plane

        # Haetaan arvot muuttujille, jotka vaikuttavat lennon kulutukseen
        weather_modifier = get_weather_modifier("mod", weathers[choice])
        travel_distance = distances[choice]
        plane_modifier = get_plane(travel_distance, "mod")
        # Lasketaan lopullinen kulutus
        co2_consumed = calculate_consumption(distance, weather_modifier, plane_modifier)

        # Katsotaan onko kaikissa maanosissa käyty
        if get_from_database(connection, "continents_visited", "player", "where screen_name = " + sceen_name) >= 7:
            break

        # Päivitetään tiedot keskeneräisenä tietokantaan
        update_database(sceen_name, co2_consumed, travel_distance)

    end_screen()
