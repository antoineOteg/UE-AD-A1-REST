from flask import Flask, render_template, request, jsonify, make_response
import requests
import time
import json

app = Flask(__name__)

### config var ###

PORT = 3203
HOST = '0.0.0.0'
moviePort = 3200
bookingPort = 3201
showtime = 3202

###           ###

# function to avoid duplicate codes
def request_service(method, path):
    try:
        req = method(path, json=request.get_json())
        return make_response(jsonify(req.json()), req.status_code)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

# get all users
@app.route("/users", methods=['GET'])
def get_all():
    return make_response(jsonify(users), 200)


# create user by url attribut name
@app.route("/users", methods=['POST'])
def create_user():
    req = request.get_json()
    if (req["name"] is None):
        return make_response(jsonify({"error": "attribut name missing"}), 400)
    id = req["name"].lower().replace(" ", "_")
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify({"error": "user ID already exists"}), 409)
    name = req["name"].lower().title()
    lastActive = int(time.time())
    res = {
        "id": id,
        "name": name,
        "last_active": lastActive
    }
    users.append(res)
    return make_response(jsonify(res), 200)

# get a users by an id
@app.route("/users/<id>", methods=['GET'])
def get_user_byid(id):
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "user ID don't exists"}), 400)


# create or update a user regarding id
@app.route("/users/<id>", methods=['PUT'])
def create_update_user(id):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(id):
            if "name" in req:
                user["name"] = req["name"]
            if "last_active" in req:
                user["last_active"] = req["last_active"]
            return make_response(jsonify(req), 200)
    req["id"] = id
    return create_user()


# delete a user regarding id
@app.route("/users/<id>", methods=['DELETE'])
def delete_user_by_id(id):
    for i, user in enumerate(users):
        if str(user["id"]) == str(id):
            tmpUser = user
            del users[i]
            return make_response(jsonify(tmpUser), 200)
    return make_response(jsonify({"error": "there is no user to delete for this id"}), 400)


# movie delegation

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    return request_service(requests.get, f"http://{HOST}:{moviePort}/movies/{movieid}")


@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    return request_service(requests.get, f"http://{HOST}:{moviePort}/moviesbytitle")


@app.route("/moviesbyDirector/<movieDirector>", methods=['GET'])
def get_movie_byDirector(movieDirector):
    return request_service(requests.get, f"http://{HOST}:{moviePort}/moviesbyDirector/{movieDirector}")


@app.route("/movies", methods=['POST'])
def create_movie(movieid):
    return request_service(requests.post, f"http://{HOST}:{moviePort}/movies/{movieid}")


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    return request_service(requests.put, f"http://{HOST}:{moviePort}/movies/{movieid}/{rate}")


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    return request_service(requests.delete, f"http://{HOST}:{moviePort}/movies/{movieid}")


# showtimes delegation

@app.route("/showtimes", methods=['GET'])
def get_schedule():
    return request_service(requests.get, f"http://{HOST}:{showtime}/showtimes")


@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    return request_service(requests.get, f"http://{HOST}:{showtime}/showmovies‹/{date}")

# booking delegation

@app.route("/user/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    return request_service(requests.get, f'http://{HOST}:{bookingPort}/bookings/{userid}')


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
