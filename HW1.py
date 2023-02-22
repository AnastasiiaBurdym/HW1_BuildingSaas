from flask import Flask, request, jsonify
import requests
from datetime import datetime

API_TOKEN = "nnn"

app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def home():
    return 'HW PYTHON Weather'


@app.route('/weather', methods=['POST'])
def get_weather():
    token = request.json.get('token')
    if token != API_TOKEN:
        raise InvalidUsage('Invalid token', status_code=401)

    city = request.json.get('city')
    date_str = request.json.get('date')

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise InvalidUsage('Invalid date format', status_code=400)

    url = 'http://api.weatherapi.com/v1/forecast.json'
    headers = {'Content-Type': 'application/json'}
    params = {
        'key': "b59bc090bc3542759fb165122231902",
        'q': city,
        'dt': date_str
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise InvalidUsage('Error getting weather data from API', status_code=500)

    weather_data = response.json()
    user_name = request.json.get('name')
    date_requested = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_data.update({
        'user_name': user_name,
        'date_requested': date_requested,
        'city': city
    })


    return jsonify(weather_data)

if __name__ == '__main__':
    app.run()
