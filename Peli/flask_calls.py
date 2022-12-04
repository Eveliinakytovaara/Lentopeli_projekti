from flask import Flask
from flask_cors import CORS

from Peli.funktiot.main_funktiot import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/newplayer/<name>/<airport>")
def newplayer(name, airport):
    connection = open_database()
    create_player(connection, name, airport)
    return '', 200


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)