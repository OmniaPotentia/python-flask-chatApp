import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load variables from the .env file
load_dotenv()


# MongoDB connection
def get_reset_token_mongo_connection():
    mongo_db_conn = os.getenv('MONGO_DB_CONNECTION')
    client = MongoClient(mongo_db_conn)
    reset_token_db = client["ResetToken"].get_collection("reset_tokens")
    return reset_token_db
