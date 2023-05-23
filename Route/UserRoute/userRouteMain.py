from flask import Blueprint
from Route.UserRoute.userRoutes import user_routes

user_route_main = Blueprint('user_route_main', __name__, url_prefix='/user')

# Register the user_routes blueprint
user_route_main.register_blueprint(user_routes)