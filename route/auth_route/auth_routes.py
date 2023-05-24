import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_wtf.csrf import generate_csrf
from werkzeug.datastructures import MultiDict

from app import csrf
from constans.http_status_constans import HTTP_STATUS_CODES
from helpers.user_encoder import UserEncoder
from helpers.validation_error import ValidationError
from middlewares.user_validation import RegistrationForm
from services.user_service import UserService

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/')


@auth_routes.route('register', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return {'csrf_token': csrf_token}


@auth_routes.route('register', methods=['POST'])
@csrf.exempt  # Exclude CSRF protection for this route
async def create_user():
    # Example: Insert a document into the collection but most likely you will be using the request.get_json() method
    # to create a user
    error_messages = []

    # Validate the request body contains JSON
    request_user_data = request.get_json()
    for_registration_validation = MultiDict(request_user_data)
    form = RegistrationForm(for_registration_validation)
    try:
        if form.validate_on_submit():

            # Access specific values from the JSON data
            username = request_user_data.get('username')
            email = request_user_data.get('email')
            password = request_user_data.get('password')
            first_name = request_user_data.get('first_name')
            last_name = request_user_data.get('last_name')
            mobile_number = request_user_data.get('mobile_number')

            existing_email = await UserService.find_by_email(email)

            if existing_email:
                existing_email_response = {
                    'status': 'error',
                    'message': 'The given email address already exists!'
                }
                return jsonify(existing_email_response), HTTP_STATUS_CODES['HTTP_BAD_REQUEST']

            created_user = UserService.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                mobile_number=mobile_number
            )
            created_user_json = json.dumps(created_user, cls=UserEncoder)
            # Generate access token
            access_token = create_access_token(identity=username)
            print(created_user)
            return jsonify({'user': created_user_json, "access_token": access_token}), HTTP_STATUS_CODES[
                'HTTP_CREATED']

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            raise ValidationError('\n'.join(error_messages))

    except ValidationError as e:
        response = {
            'status': 'error',
            'message': str(e),
        }
        return jsonify(response), HTTP_STATUS_CODES['HTTP_BAD_REQUEST']
    except Exception as e:

        # Handle the exception and return an error response

        return jsonify({'error': str(e)}), HTTP_STATUS_CODES['HTTP_BAD_REQUEST']


# Protected route (requires authentication)
@auth_routes.route('protected', methods=['GET'])
@jwt_required()  # Note the parentheses after jwt_required
def protected():
    # Access protected resource
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! This is a protected route.'}), HTTP_STATUS_CODES["HTTP_OK"]
