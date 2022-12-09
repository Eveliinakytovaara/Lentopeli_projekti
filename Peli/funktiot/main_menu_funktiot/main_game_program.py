from Peli.funktiot.peli_funktiot.peli_funktiot import *


def flight_game(starting_airport, player_index, connection):
    # Tallenetaan aloitus lentokenttä muuttjaan (ident-arvo)
    current_airport = starting_airport

    # Luodaan joukko, jolla pidetään muistissa maanosat, jossa pelaaja on käynyt
    # Joukkoihin ei tallennu kopoita, joten sen pituus on tarkka arvio, monessa maanosassa pelaaja on käynyt
    continents_visited = set()
    # Haetaan yhdessä string muutujassa mahdolliset edelliset maanosat, missä ollaan käyty
    continent_sql = get_from_database("continents_visited", "player",
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
        print(f"You are at {get_airport(current_airport, 'name')}, "
              f"{get_country(current_airport)}")
        weather = get_weather(current_airport)

        # Haetaan naapuri maanosat listaan aloitus lentoaseman maanosan perusteella
        neighbours = get_neighbouring_continents(current_airport)

        # Tulostetaan naapuri maanosat (for loop)
        print("Where would you like to fly next?")
        x = 0
        for i in neighbours:
            x += 1
            print(f"{x}: {get_continent_name(i)}")

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
        airports = get_random_airports(continent_choice, 'ident', 5)

        # Luodaan sisäänrakennettu lista (listoja lisan sisällä)
        for x in range(len(airports)):
            # Luodaan tilapäinen lista, joka sisältää ykittäisiä arvoja lentoasemasta
            # Tämä lista lisätään airport_data listan alkioksi
            temp = []
            # Haetaan lentoaseman nimi jo arvottujen lentoasemien koodien mukaan
            temp_airports = get_airport(airports[x], 'name')
            temp.append(f"{'Airport:':11s}{temp_airports}")
            # Haetaan lentoaseman maan nimi
            temp.append(f"{'Country:':11s}{get_country(airports[x])}")
            # Haetaan satunnainen säätilan nimi, mutta vain kuvaus lisätään tulostettaviin
            weather_name.append(get_random_weather("name"))
            temp.append(f"{'Weather:':11s}{get_weather('description', weather_name[-1])}")
            # Lasketaan etäisyys
            temp_distance = get_distance(current_airport, airports[x])
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
        travel_distance = get_distance(current_airport, airports[choice])
        plane_modifier = float(get_plane(travel_distance, "mod"))
        weather_modifier = float(get_weather("modifier", weather_name[choice]))

        # Lasketaan lopullinen kulutus
        co2_consumed = calculate_consumption(travel_distance, weather_modifier, plane_modifier)

        # Lisätään maanosa, jonne lennettiin, joukkoon (Joukoissa ei voi olla kopioita)
        current_continent = get_from_database("continent", "airport",
                                              "WHERE ident = '" + airports[choice] + "'")
        continents_visited.add(current_continent[0])

        # Tietokantaan ei voi lisätä listoja, joten tehdään listan arvoista string muuttuja
        # esim. on käynyt EU ja NA -> EUNA
        continent_str = ""
        for i in continents_visited:
            continent_str += i

        # Päivitetään tiedot tietokantaan
        update_player_data(player_index, co2_consumed, travel_distance,
                           get_plane(travel_distance, "name"), continent_str, airports[choice])

        # Katsotaan onko kaikissa maanosissa käyty
        if len(continents_visited) >= 7:
            break
        else:
            # jos ei, jatketaan peliä ilmoittamalla, että missä on käynyt
            print("You have visited the following continents: ")
            for i in continents_visited:
                print(get_continent_name(i))

        # Päivitetään uusi lentoasema
        current_airport = airports[choice]

    if len(continents_visited) >= 7:
        screen_name = get_from_database("screen_name", "player", f"where id = '{player_index}'")
        co2_consumed = get_from_database("co2_consumed", "player", f"where id = '{player_index}'")
        travel_distance = get_from_database("travel_distance", "player", f"where id = '{player_index}'")
        starting_location = get_from_database("starting_location", "player", f"where id = '{player_index}'")
        s_planes_used = get_from_database("s_planes_used", "player", f"where id = '{player_index}'")
        m_planes_used = get_from_database("m_planes_used", "player", f"where id = '{player_index}'")
        l_planes_used = get_from_database("l_planes_used", "player", f"where id = '{player_index}'")
        end_screen(screen_name[0], co2_consumed[0], travel_distance[0], starting_location[0],
                   s_planes_used[0], m_planes_used[0], l_planes_used[0])
