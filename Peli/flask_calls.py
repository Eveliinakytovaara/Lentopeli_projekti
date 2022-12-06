from flask import Flask
from flask_cors import CORS
import json

from Peli.funktiot.main_menu_funktiot.main_menu_funktiot import *
from Peli.funktiot.main_menu_funktiot.main_game_program import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/newplayer/<name>/<airport>")
def newplayer(name, airport):
    connection = open_database()
    create_player(connection, name, airport)
    answer = {
        'name': name,
        'id': get_from_database(connection, 'id', 'player', f'where screen_name = "{name}"')
    }
    data = json.dumps(answer)
    return data


@app.route("/cleardata")
def cleardata():
    c = open_database()
    clear_player_data(c)
    return '', 200


@app.route('/getplayer/<id>')
def getplayer(id):
    c = open_database()
    answer = {
        'id': id,
        'name': get_from_database(c, 'screen_name', 'player', f'where id = "{id}"')[0],
        'co2_consumed': get_from_database(c, 'co2_consumed', 'player', f'where id = "{id}"')[0],
        'travel_distance': get_from_database(c, 'travel_distance', 'player', f'where id = "{id}"')[0],
        'location': get_from_database(c, 'location', 'player', f'where id = "{id}"')[0],
        'starting_location': get_from_database(c, 'starting_location', 'player', f'where id = "{id}"')[0],
        'number_of_flights': get_from_database(c, 'number_of_flights', 'player', f'where id = "{id}"')[0],
        's_planes_used': get_from_database(c, 's_planes_used', 'player', f'where id = "{id}"')[0],
        'm_planes_used': get_from_database(c, 'm_planes_used', 'player', f'where id = "{id}"')[0],
        'l_planes_used': get_from_database(c, 'l_planes_used', 'player', f'where id = "{id}"')[0],
        'continents_visited': get_from_database(c, 'continents_visited', 'player', f'where id = "{id}"')[0]
    }
    data = json.dumps(answer)
    return data


@app.route('/updateplayer/<id>/<column>/<value>')
def updatePlayer(id, column, value):
    c = open_database()
    update_player(c, id, column, value)
    return "", 200


@app.route('/gethighscores')
def gethighscores():
    c = open_database()
    complete_games = get_from_database(c, "id, screen_name, co2_consumed, travel_distance, "
                                          "number_of_flights, s_planes_used, m_planes_used,"
                                          " l_planes_used"
                                       , "player",
                                       "where CHAR_LENGTH(continents_visited) >= 14 "
                                       "ORDER BY co2_consumed ASC")

    answer = {}
    for i in range(len(complete_games)):
        splitlist = complete_games[i].split()
        name = get_from_database(c, 'screen_name', 'player', f'where id = {splitlist[0]}')[0]
        print(name)
        entry = {
            'number': i,
            'name': name,
            'co2_consumed': splitlist[2],
            'travel_distance': splitlist[3],
            'number_of_flights': splitlist[4],
            's_planes_used': splitlist[5],
            'm_planes_used': splitlist[6],
            'l_planes_used': splitlist[7]
        }
        print(entry)
        answer.update({
            i: entry
        })
    data = json.dumps(answer)
    return data


@app.route("/randairport/<count>")
@app.route("/randairport/<count>/<continent>")
def randairport(count, continent=''):
    c = open_database()
    airports = get_random_airports(c, continent, 'ident', count)
    answer = {}
    for i in range(int(count)):
        entry = {
            'ident': airports[i],
            'name': get_from_database(c, 'name', 'airport', f'where ident = "{airports[i]}"')[0],
            'region': get_from_database(c, 'iso_region', 'airport', f'where ident = "{airports[i]}"')[0],
            'lat': get_from_database(c, 'latitude_deg', 'airport', f'where ident = "{airports[i]}"')[0],
            'lon': get_from_database(c, 'longitude_deg', 'airport', f'where ident = "{airports[i]}"')[0],
            'continent': get_from_database(c, 'continent', 'airport', f'where ident = "{airports[i]}"')[0],
            'country_code': get_from_database(c, 'iso_country', 'airport', f'where ident = "{airports[i]}"')[0],
            'country_name': get_country(c, airports[i])
        }
        answer.update({
            i: entry
        })
    jsondata = json.dumps(answer)
    return jsondata


@app.route('/getairport/<ident>')
def getairport(ident):
    c = open_database()
    answer = {
        'ident': ident,
        'name': get_from_database(c, 'name', 'airport', f'where ident = "{ident}"')[0],
        'region': get_from_database(c, 'iso_region', 'airport', f'where ident = "{ident}"')[0],
        'lat': get_from_database(c, 'latitude_deg', 'airport', f'where ident = "{ident}"')[0],
        'lon': get_from_database(c, 'longitude_deg', 'airport', f'where ident = "{ident}"')[0],
        'continent': get_from_database(c, 'continent', 'airport', f'where ident = "{ident}"')[0],
        'country_code': get_from_database(c, 'iso_country', 'airport', f'where ident = "{ident}"')[0],
    }
    jsondata = json.dumps(answer)
    return jsondata


# TODO: fix continent searching to make more sense
@app.route('/getcontinent/<ident>')
def getcontinent(ident):
    c = open_database()
    c_code = get_from_database(c, 'continent', 'airport', f'where ident = "{ident}"')[0]
    neigbours = get_neighbouring_continents(c, ident)
    answer = {
        'continent': {
            'code': c_code,
            'name': get_continent_name(c, c_code)
        },
        'n1': {
            'code': neigbours[0],
            'name': get_continent_name(c, neigbours[0])
        },
        'n2': {
            'code': neigbours[1],
            'name': get_continent_name(c, neigbours[1])
        },
        'n3': {
            'code': neigbours[2],
            'name': get_continent_name(c, neigbours[2])
        },
        'n4': {
            'code': neigbours[3],
            'name': get_continent_name(c, neigbours[3])
        }
    }
    jsondata = json.dumps(answer)
    return jsondata


@app.route("/getdistance/<aAirport>/<bAirport>")
def getdistance(aAirport, bAirport):
    c = open_database()
    answer = {
        'distance': get_distance(c, aAirport, bAirport)
    }
    data = json.dumps(answer)
    return data


# TODO: currently returns only a name. Add more data if necessary or merge with other functions
@app.route('/getcountry/<ident>')
def getcountry(ident):
    c = open_database()
    name = get_country(c, ident)
    answer = {'name': name}
    jsondata = json.dumps(answer)
    return jsondata


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
