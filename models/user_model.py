import datetime
import os
import random

import bcrypt
from dotenv import load_dotenv
from mongoengine import Document, StringField, BooleanField, EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import connect

# Load variables from the .env file
load_dotenv()
# Establish a connection to MongoDB
connect(os.getenv('USER_DB'), host=os.getenv('MONGO_DB_CONNECTION'), port=int(os.getenv('MONGO_DB_PORT')))


class OAuthProfile(EmbeddedDocument):
    provider = StringField()
    profileId = StringField()


class User(Document):
    username = StringField(required=True, unique=True, min_length=6)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    mobile_number = StringField(unique=True)
    verified = BooleanField(default=False)
    verification_token = StringField(required=True, unique=True,
                                     default=lambda: str(100000 + random.randint(0, 900000)))
    active_status = BooleanField(default=False)
    oauth_profiles = EmbeddedDocumentListField(OAuthProfile)
    created_at = StringField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    last_updated_at = StringField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    meta = {
        'indexes': [
            {'fields': ['oauth_profiles.provider', 'oauth_profiles.profileId']}
        ]
    }

    @classmethod
    def generate_hash(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('$2b$'):
            self.password = self.generate_hash(self.password)
        return super(User, self).save(*args, **kwargs)