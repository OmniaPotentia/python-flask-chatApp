from flask import Blueprint

from route.auth_route.auth_route_main import auth_route_main

route_blueprint = Blueprint('route', __name__)

# Register the user_route_main blueprint
route_blueprint.register_blueprint(auth_route_main)
