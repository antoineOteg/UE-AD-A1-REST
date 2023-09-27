from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():   
   print(bookings)
   return make_response(jsonify(bookings), 200)

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid: str):
   
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
   return make_response(jsonify({"error":"User ID not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid: str):
   req = request.get_json()

   booking = None
   for el in bookings:
      if str(el["userid"]) == str(userid):
         booking = el
         break

   if booking is None:
      return make_response(jsonify({"error":"User ID not found"}),400)
   
   for date in booking["dates"]:
      if str(date["date"]) == str(req["date"]):
         date["movies"].append(req["movieid"])
         return make_response(jsonify({"message":"booking added"}),200)

   booking["dates"].append({"date": str(req["date"]), "movies": [str(req["movieid"])]})
   return make_response(jsonify({"message":"booking added"}),200)




if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
