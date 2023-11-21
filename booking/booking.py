from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

# global variables about the service
PORT = 3201
HOST = '0.0.0.0'
showtimePort = 3202

# load database
with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


# welcome page
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# get all bookings
@app.route("/bookings", methods=['GET'])
def get_json():
    return make_response(jsonify(bookings), 200)


# get all bookings of user by its id
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid: str):
    # search booking in database
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking), 200)
            return res
    return make_response(jsonify({"error": "User ID not found"}), 400)


# add new booking for a user
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid: str):
    # get booking informations
    req = request.get_json()
    movieid = str(req["movieid"])
    moviedate = str(req["date"])

    # check if there's a showtime for the requested movie and date by contacting the showtime service
    try:
        showtime = requests.get(f"http://{HOST}:{showtimePort}/showmovies/{moviedate}")
    except Exception as e:
        # print(e)
        return make_response(jsonify({"error": f'error when requesting showtime'}), 400)

    if showtime.status_code != 200 or movieid not in showtime.json()["movies"]:
        return make_response(jsonify({"error": "no showtime found for this booking"}), 400)

    # find correct user in bookings
    booking = None
    for el in bookings:
        if str(el["userid"]) == str(userid):
            booking = el
            break

    if booking is None:
        return make_response(jsonify({"error": "User ID not found"}), 400)

    # find correct date in the user's bookings
    for date in booking["dates"]:
        if str(date["date"]) == moviedate:
            date["movies"].append(movieid)
            return make_response(jsonify({"message": "booking added"}), 200)

    # add new booking to user
    new = {"date": moviedate, "movies": [movieid]}
    booking["dates"].append(new)
    return make_response(jsonify(new), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
