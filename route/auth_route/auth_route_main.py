from flask import Blueprint

from route.auth_route.auth_routes import auth_routes

auth_route_main = Blueprint('auth_route_main', __name__, url_prefix='/auth')

# Register the user_routes blueprint
auth_route_main.register_blueprint(auth_routes)
