from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# global variables about the movie service
PORT = 3200
HOST = '0.0.0.0'

# load database
with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


# welcome page
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


# Get all movies
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


# Get a movie by its id
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    # search for movie in database
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


# Get a movie by its title
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        # search for movie in database
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


# Get all movies from a director
@app.route("/moviesbyDirector/<movieDirector>", methods=['GET'])
def get_movie_byDirector(movieDirector):
    # search movies in database
    res = [mov for mov in movies if str(mov["director"]) == str(movieDirector)]
    if len(res) != 0:
        return make_response(jsonify(res), 200)
    return make_response(jsonify({"error": "no movies for this director"}), 400)


# Create new movie
@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    # check if id already exists
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    req['id'] = movieid
    movies.append(req)
    res = make_response(jsonify(req), 200)
    return res


# Update a movie's rating
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    # search movie in database
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            # update rating
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


# Delete movie with its id
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    # search movie in database
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            # remove movie
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
