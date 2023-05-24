import json

from bson import ObjectId


# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)
