# UE-AD-A1-REST

## Structure of the project

The project contains 4 REST microservices as shown below :

![services.png](assets%2Fservices.png)

The goal of this project is to understand how REST Api communicate 
and create a simple application where users can book to see a movie.

Each service stores data in a JSON file and provides a OpenAPI file which gives you all the informations about the different routes it can offer.
The file in question is named UE-archi-distribuees-NameOfTheService-Version.yaml. 


### User Service

Located in the /user folder. This service manages the users (create, read, update and delete). All the routes
are accessible via HTTP. This service is the entreypoint to the whole system 
and interacts with the other services. 

### Movie Service

Located in the /movie folder. This service gives CRUD functionalities regarding Movies.   

### Booking Service

Located in the /booking folder. This service is used to manage the bookings to the movies each user want to see.  

### Times Service

Located in the /showtime folder. Contains all the informations and CRUD functionnalities about 
showtimes for the movies. 

## How to deploy

To deploy the project, clone this repository on your machine.


Each service must be started manually.

Open four command terminals in each microservice folder user, movie, booking and showtime. 

Then, run these commands in order and in the correct terminal :
```
python3 user.py
```
```
python3 movie.py
```
```
python3 booking.py
```
```
python3 showtime.py
```

### Access Services

By default, services are accessible on the following ips :

- User : 127.0.0.1:3203
- Booking : 127.0.0.1:3201
- Movie : 127.0.0.1:3200
- Showtime : 127.0.0.1:3202

Postman Collections are available in the folder /postman for you to test endpoints.