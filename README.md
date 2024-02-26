# Tank and Profile API

## Summary
This code provides an API for managing tanks and profiles using FastAPI and MongoDB. It includes the following features:

### Tank Model
- `Tank` class represents the model for a tank and includes fields such as location, latitude, and longitude.

### Profile Model
- `Profile` class represents the model for a user profile and includes fields for last update time, username, role, and color.

### Endpoints
1. `GET /profile`: Retrieves a list of profiles from the database.
2. `POST /profile`: Creates a new profile in the database.
3. `GET /tank`: Retrieves a list of tanks from the database.
4. `GET /tank/{id}`: Retrieves a specific tank by its ID.
5. `POST /tank`: Creates a new tank in the database.
6. `PATCH /tank/{id}`: Updates an existing tank by its ID.
7. `DELETE /tank/{id}`: Deletes a tank by its ID.

### Update Profile Function
- `update_profile` function updates the last update time of the profiles in the database.

## Purpose
The code was written to provide a RESTful API for managing tanks and profiles in a MongoDB database using FastAPI. It allows for CRUD (Create, Read, Update, Delete) operations on tanks and profiles.

The API can be used to integrate tank and profile management functionality into web or mobile applications.

## Two Truths and a Lie
1. I cannot swim
2. I use three phones everyday
3. I dont hate anyone

Can you guess which one is the lie?
