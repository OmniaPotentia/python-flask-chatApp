from flask import Blueprint, jsonify
# from ..Database.userDB import getMongoConnection

user_routes = Blueprint('user_routes', __name__, url_prefix='/profile')

# userCollection = getMongoConnection()


@user_routes.route('/list')
def hello():
    return "Hello World!"
    # results = []
    # cursor = userCollection.find()
    # for document in cursor:
        # document['_id'] = str(document['_id'])  # Serialize ObjectId to string
        # results.append(document)
    # return jsonify(results)


@user_routes.route('/create')
def writeDb():
    # Example: Insert a document into the collection
    document = {"name": "John Doe", "age": 30, "city": "New York"}
    result = userCollection.insert_one(document)

    return f"Document inserted with ID: {result.inserted_id}"