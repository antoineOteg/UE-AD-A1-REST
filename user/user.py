from flask import Flask, render_template, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
bookingPort = 3201

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/user/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    try:
        bookings = requests.get(f'http://{HOST}:{bookingPort}/bookings/{userid}')
        print(bookings)
        return make_response(bookings.json(), bookings.status_code)
    except:
        return make_response(jsonify({"error": "error when requesting booking"}), 400)

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
