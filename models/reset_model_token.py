import hashlib
import uuid
from datetime import datetime

from database.reset_token_db import get_reset_token_mongo_connection

reset_token_db = get_reset_token_mongo_connection()


class ResetToken:
    def __init__(self, user_id):
        self.user_id = user_id
        self.token = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
        self.created_at = datetime.now()

    def save(self):
        reset_token_db.insert_one({
            'user_id': self.user_id,
            'token': self.token,
            'created_at': self.created_at
        })

    @staticmethod
    def find_by_user_id(user_id):
        return reset_token_db.find_one({'user_id': user_id})

    @staticmethod
    def delete_by_token(token):
        reset_token_db.delete_one({'token': token})
