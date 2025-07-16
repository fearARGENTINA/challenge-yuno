from flask import Blueprint, jsonify
from controllers.user import UserController
from flask_pydantic import validate
from schemas.user import UserCreate, UserSearch, UserUpdate
from decorators.token import tokenRequired
from config.config import Role
userRoute = Blueprint('user', __name__)

@userRoute.route('/user/<id>', methods=['GET'])
@tokenRequired(Role.ADMIN, Role.USER)
@validate()
def get_user(id: int):
    try:
        return UserController().getUser(id)
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened', 'error': str(e)})

@userRoute.route('/users', methods=['GET'])
@tokenRequired(Role.ADMIN, Role.USER)
@validate()
def search_users(body: UserSearch):
    try:
        return UserController().searchUsers(body)
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened', 'error': str(e)})

@userRoute.route('/user', methods=['POST'])
@tokenRequired(Role.ADMIN)
@validate()
def create_user(body: UserCreate):
    try:
        return UserController().createUser(body)
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened'})

@userRoute.route('/user/<id>', methods=['PUT'])
@tokenRequired(Role.ADMIN)
@validate()
def update_user(id: int, body: UserUpdate):
    try:
        return UserController().updateUser(id, body)
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened'})
