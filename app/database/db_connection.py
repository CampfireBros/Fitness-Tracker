from pymongo import MongoClient
import config

##
# creates a connection to the remote Mongo DB
# and sets up variables for each collection we use
client = MongoClient(config.MONGODB_URL)
db = client.exercisedb
user_collection = db.Users
exercise_collection = db.Exercises
