from flask import Flask, Response
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/Kok/<koodi>")
def Kok(koodi):
    answer = {
        "status": 'hey',
        "luku1": 'hoi',
        "luku2": 'hello',
        "summa": 'mor'
    }
    if koodi != '0':
        print('joo')
    else:
        print('ei')
    jsonvast = json.dumps(answer)
    return jsonvast


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
