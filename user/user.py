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
showtimePort = 3202

###           ###

# execute a request method with json
def request_service(method, path):
    try:
        req = method(path, json=request.get_json())
        return make_response(jsonify(req.json()), req.status_code)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


# load database
with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


# welcome page
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

# get all users
@app.route("/users", methods=['GET'])
def get_all():
    return make_response(jsonify(users), 200)


# create user with json body
@app.route("/users", methods=['POST'])
def create_user():
    # get id of new user
    req = request.get_json()
    if (req["name"] is None):
        return make_response(jsonify({"error": "attribute name missing"}), 400)
    id = req["name"].lower().replace(" ", "_")

    # check if id already exists
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify({"error": "user ID already exists"}), 409)
    name = req["name"].lower().title()

    # create user
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
    # search user in database
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "user ID doesn't exists"}), 400)


# create or update a user's name and/or last_active
@app.route("/users/<id>", methods=['PUT'])
def create_update_user(id):
    req = request.get_json()
    # search user in database
    for user in users:
        if str(user["id"]) == str(id):

            # update name and last_active if present in body
            if "name" in req:
                user["name"] = req["name"]
            if "last_active" in req:
                user["last_active"] = req["last_active"]
            return make_response(jsonify(req), 200)
    req["id"] = id
    # create a user if it doesn't already exist
    return create_user()


# delete a user with its id
@app.route("/users/<id>", methods=['DELETE'])
def delete_user_by_id(id):
    # search user in database
    for i, user in enumerate(users):
        if str(user["id"]) == str(id):
            # delete user
            tmpUser = user
            del users[i]
            return make_response(jsonify(tmpUser), 200)
    return make_response(jsonify({"error": "there is no user to delete for this id"}), 400)


# call movie service to get a movie by its id
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    return request_service(requests.get, f"http://movie:{moviePort}/movies/{movieid}")


# call movie service to get a movie by its title
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    return request_service(requests.get, f"http://movie:{moviePort}/moviesbytitle")


# call movie service to get all movies made by a specific director
@app.route("/moviesbyDirector/<movieDirector>", methods=['GET'])
def get_movie_byDirector(movieDirector):
    return request_service(requests.get, f"http://movie:{moviePort}/moviesbyDirector/{movieDirector}")


# call movie service to create a new movie
@app.route("/movies", methods=['POST'])
def create_movie(movieid):
    return request_service(requests.post, f"http://movie:{moviePort}/movies/{movieid}")


# call movie service to update a movie rating
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    return request_service(requests.put, f"http://movie:{moviePort}/movies/{movieid}/{rate}")


# call movie service to delete a movie
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    return request_service(requests.delete, f"http://movie:{moviePort}/movies/{movieid}")


# call showtime service to get all showtimes
@app.route("/showtimes", methods=['GET'])
def get_schedule():
    return request_service(requests.get, f"http://showtime:{showtimePort}/showtimes")


# call showtime service to get all showtimes on a specific date
@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    return request_service(requests.get, f"http://booking:{showtimePort}/showmovies‹/{date}")


# call booking service to get all bookings of a specific user
@app.route("/user/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    return request_service(requests.get, f'http://booking:{bookingPort}/bookings/{userid}')


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host='0.0.0.0', port=PORT)
