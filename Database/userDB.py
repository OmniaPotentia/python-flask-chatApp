from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()


# MongoDB connection
def getMongoConnection():
    mongoDBConn = os.getenv('MONGODBCONNECTION')
    client = MongoClient(mongoDBConn)
    userDB = client["Users"].get_collection("user")
    return userDB
