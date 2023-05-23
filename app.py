from flask import Flask, jsonify
from Route.route import route_blueprint
from Helpers.customJsonEncoderhelpers import CustomJSONEncoder

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

# Register the route blueprint
app.register_blueprint(route_blueprint)

if __name__ == '__main__':
    app.run()
