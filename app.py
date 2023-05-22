from flask import Flask, jsonify
from Database.userDB import getMongoConnection
from Helpers.customJsonEncoderhelpers import CustomJSONEncoder

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
userCollection = getMongoConnection()


@app.route('/')
def hello():
    results = []
    cursor = userCollection.find()
    for document in cursor:
        document['_id'] = str(document['_id'])  # Serialize ObjectId to string
        results.append(document)
    return jsonify(results)


@app.route('/post')
def writeDb():
    # Example: Insert a document into the collection
    document = {"name": "John Doe", "age": 30, "city": "New York"}
    result = userCollection.insert_one(document)

    return f"Document inserted with ID: {result.inserted_id}"


if __name__ == '__main__':
    app.run(debug=True)
