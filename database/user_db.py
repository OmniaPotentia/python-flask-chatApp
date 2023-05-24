import os

from dotenv import load_dotenv
from pymongo import MongoClient
from mongoengine import connect
# Load variables from the .env file
load_dotenv()


# MongoDB connection
def get_user_mongo_connection():
    mongo_db_conn = os.getenv('MONGO_DB_CONNECTION')
    client = MongoClient(mongo_db_conn)
    user_db = client["Users"].get_collection("user")
    return user_db
