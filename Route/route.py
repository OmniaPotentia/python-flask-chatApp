from flask import Blueprint
from Route.UserRoute.userRouteMain import user_route_main

route_blueprint = Blueprint('route', __name__)

# Register the user_route_main blueprint
route_blueprint.register_blueprint(user_route_main)