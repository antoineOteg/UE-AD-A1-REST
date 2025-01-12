from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

### config var ###

PORT = 3202
HOST = '0.0.0.0'

###           ###

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

# get all schedule
@app.route("/showtimes", methods=['GET'])
def get_schedule():
    res = make_response(jsonify(schedule), 200)
    return res


# get a schedule regarding a date
@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    for sched in schedule:
        if str(sched["date"]) == str(date):
            return make_response(jsonify(sched), 200)
    return make_response(jsonify({"error": "bad input parameter"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
