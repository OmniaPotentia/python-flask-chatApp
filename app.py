import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_wtf import CSRFProtect

from helpers.custom_json_encoder_helpers import CustomJSONEncoder

load_dotenv()

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

# Override configuration with environment variables
app.config['SECRET_KEY'] = os.getenv('MY_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('MY_JWT_SECRET_KEY')
jwt = JWTManager(app)

csrf = CSRFProtect(app)

# Enable CSRF protection
csrf.init_app(app)

if __name__ == '__main__':
    # Importing route_blueprint here to avoid circular import
    from route.route import route_blueprint

    # Register the route blueprint
    app.register_blueprint(route_blueprint)
    app.run()
