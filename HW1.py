# import Flask, request та jsonify from Flask library.
from flask import Flask, request, jsonify

import requests
# import datetime function to work with the date
from datetime import datetime

# API token required for authentication
API_TOKEN = "your_api_token"

app = Flask(__name__)


# class for handling invalid usage exceptions
class InvalidUsage(Exception):
    status_code = 400

    # initialize the class
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    # method to convert the class object to a dictionary.
    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


# an error handler that returns a response object with a JSON representation of the error message and status code.
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# a route function that returns a string when the application root is accessed.
@app.route('/')
def home():
    return 'HW PYTHON Weather'


# a route function that handles the HTTP POST request. It first checks if the API token in the request matches the API_TOKEN variable, and raises an InvalidUsage exception with a 401 status code if they don't match. It then constructs a request URL and parameters to make a request to the weather API using the requests library. It then retrieves the JSON response and adds the user_name and date_requested fields to the JSON response, which it returns to the client.
@app.route('/weather', methods=['POST'])
def get_weather():
    token = request.json.get('token')
    if token != API_TOKEN:
        raise InvalidUsage('Invalid token', status_code=401)

    url = 'http://api.weatherapi.com/v1/forecast.json'
    headers = {'Content-Type': 'application/json'}
    params = {
        'key': 'your_key',
        'q': request.json.get('city'),
        'days': request.json.get('days')
    }
    response = requests.get(url, headers=headers, params=params)
    weather_data = response.json()
    user_name = request.json.get('name')
    date_requested = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_data.update({
        'user_name': user_name,
        'date_requested': date_requested
    })
    return jsonify(weather_data)


# runs the application if it is being run as a standalone Python script.
if __name__ == '__main__':
    app.run()
