from flask import Flask
from flask_cors import CORS
import json

from Peli.kokeiluja.flight_game_and_functions import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/newplayer/<name>/<airport>")
def newplayer(name, airport):
    connection = open_database()
    create_player(connection, name, airport)
    answer = {
        name: "created"
    }
    data = json.dumps(answer)
    return data


@app.route("/randairport/<count>")
def randairport(count):
    c = open_database()
    airports = get_random_airports(c, '', 'ident', count)
    answer = {}
    for i in range(int(count)):
        entry = {
            'ident': airports[i],
            'name': get_from_database(c, 'name', 'airport', f'where ident = "{airports[i]}"')[0],
            'region': get_from_database(c, 'iso_region', 'airport', f'where ident = "{airports[i]}"')[0],
            'lat': get_from_database(c, 'latitude_deg', 'airport', f'where ident = "{airports[i]}"')[0],
            'lon': get_from_database(c, 'longitude_deg', 'airport', f'where ident = "{airports[i]}"')[0],
            'continent': get_from_database(c, 'continent', 'airport', f'where ident = "{airports[i]}"')[0],
            'country_code': get_from_database(c, 'iso_country', 'airport', f'where ident = "{airports[i]}"')[0]
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
        'country_code': get_from_database(c, 'iso_country', 'airport', f'where ident = "{ident}"')[0]
    }
    jsondata = json.dumps(answer)
    return jsondata


# TODO: fix continent searching to make more sense
@app.route('/getcontinent/<code>')
def getcontinent(code):
    c = open_database()
    c_code = get_from_database(c, 'continent', 'airport', f'where ident = "{code}"')[0]
    neigbours = get_neighbouring_continents(c, code)
    answer = {
        'continent': c_code,
        'neighbour_1': neigbours[0],
        'neighbour_2': neigbours[1],
        'neighbour_3': neigbours[2],
        'neighbour_4': neigbours[3],
        'name': get_continent_name(c, c_code)
    }
    jsondata = json.dumps(answer)
    return jsondata


# TODO: currently returns only a name. Add more data if necessary or merge with other functions
@app.route('/getcountry/<ident>')
def getcountry(ident):
    c = open_database()
    name = get_country(c, ident)
    answer = {'name': name}
    jsondata = json.dumps(answer)
    return jsondata


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
