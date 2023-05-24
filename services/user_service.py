from random import getrandbits

from database.async_user_db import get_async_user_mongo_connection
from database.reset_token_db import get_reset_token_mongo_connection
from models.reset_model_token import ResetToken
from models.user_model import User

reset_token_collection = get_reset_token_mongo_connection()
async_user_collection = get_async_user_mongo_connection()


class UserService:
    @staticmethod
    async def find_by_email(email):
        found_email = await async_user_collection.find_one({'email': email})
        return found_email

    @staticmethod
    async def find_by_mobile_number(mobile_number):
        found_mobile_number = await async_user_collection.find_one({'mobile_number': mobile_number})
        return found_mobile_number

    @staticmethod
    async def find_by_username(username):
        found_username = await async_user_collection.find_one({'username': username})
        return found_username

    @staticmethod
    def create_user(username, first_name, last_name, email, password, mobile_number):
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            mobile_number=mobile_number
        )
        inserted_user = user.save()
        return inserted_user

    @staticmethod
    async def change_status(user):
        query = {}
        if user['email']:
            query = {'email': user['email']}
        elif user['mobile_number']:
            query = {'mobile_number': user['mobile_number']}
        else:
            query = {'username': user['username']}
        user['active_status'] = False if user['active_status'] else True
        await async_user_collection.update_one(query, {'$set': {'active_status': user['active_status']}})

    @staticmethod
    async def create_google_user(username, email, oauth_profile):
        user = {
            'username': username,
            'email': email,
            'oauth_profiles': [oauth_profile],
            'password': str(getrandbits(10)),
        }
        await async_user_collection.insert_one(user)
        return user

    @staticmethod
    async def create_password_reset_token(user_id):
        token = ResetToken(user_id)
        await token.save()
        return token.token

    @staticmethod
    async def verify_password_reset_token(user_id, token):
        return await reset_token_collection.find_one({'user_id': user_id, 'token': token})

    @staticmethod
    async def delete_password_reset_token(token):
        await reset_token_collection.delete_one({'token': token})

    @staticmethod
    async def change_password(user_id, password):
        user = await async_user_collection.find_one({'_id': user_id})
        if not user:
            raise ValueError('User not found')
        user['password'] = password
        await async_user_collection.save(user)
        return user

    @staticmethod
    async def find_by_oauth_profile(provider, profile_id):
        return await async_user_collection.find_one(
            {'oauth_profiles.provider': provider, 'oauth_profiles.profileId': profile_id})

    @staticmethod
    async def get_reset_token(user_id):
        return await reset_token_collection.find_one({'user_id': user_id})

    @staticmethod
    async def get_list():
        return await async_user_collection.find().sort('createdAt', -1).to_list()

    @staticmethod
    async def delete_user(user_id):
        await async_user_collection.delete_one({'_id': user_id})

    @staticmethod
    async def add_username(user, username):
        await async_user_collection.update_one({'email': user}, {'$set': {'username': username}})
