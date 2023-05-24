import json

from models.user_model import User


class UserEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            # Convert the User object to a dictionary
            user_dict = {
                "id": str(o.id),
                "username": o.username,
                "first_name": o.first_name,
                "last_name": o.last_name,
                "email": o.email,
                "password": o.password,
                "mobile_number": o.mobile_number,
                "verified": o.verified,
                "verification_token": o.verification_token,
                "active_status": o.active_status,
                "oauth_profiles": o.oauth_profiles,
            }
            return user_dict
        return super().default(o)
