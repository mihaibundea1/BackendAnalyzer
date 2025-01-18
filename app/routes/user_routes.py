from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_routes = Blueprint('users', __name__)

# Ruta corectă pentru localhost:5000/users pentru GET
@user_routes.route('/', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return jsonify([user.serialize() for user in users])

# Ruta pentru localhost:5000/users/<user_id> pentru GET un utilizator specific
@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user.serialize())
    return jsonify({'error': 'User not found'}), 404

# Ruta pentru POST pe /users pentru a crea un utilizator
@user_routes.route('/', methods=['POST'])
def create_user():
    data = request.json
    new_user = UserService.create_user(data)
    return jsonify(new_user.serialize()), 201

# Ruta pentru PUT pe /users/<user_id> pentru a actualiza un utilizator
@user_routes.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    updated_user = UserService.update_user(user_id, data)
    if updated_user:
        return jsonify(updated_user.serialize())
    return jsonify({'error': 'User not found'}), 404

# Ruta pentru DELETE pe /users/<user_id> pentru a șterge un utilizator
@user_routes.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404
