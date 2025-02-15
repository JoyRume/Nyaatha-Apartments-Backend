from flask import Blueprint, jsonify, request, current_app
from models import User
from config import Config, token_required, role_required

userBluePrint = Blueprint('user', __name__)

# For admins only
@userBluePrint.route('/users', methods=['GET'])
@token_required
@role_required("Admin")
def get_all_users():
    users = current_app.mongo.db.users.find()
    
    user_list = [
        {
            'id': str(user['_id']),  
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'phone_number': user['phone_number']
        }
        for user in users
    ]
    
    return jsonify(user_list), 200

# Getting the user profile
@userBluePrint.route('/profile', methods=['GET'])
@token_required
def get_profile():
    user_id = request.user["user_id"]
    user = User.get_user_by_id(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "phone_number": user["phone_number"]
    }), 200

@userBluePrint.route('/token', methods=['POST'])
def generate_token():
    data = request.json
    user_identifier = data.get("user_id")
    role = data.get("role")
    
    if not user_identifier or not role:
        return jsonify({"message": "User ID and Role are required"}), 400
    
    token = Config.generate_jwt(user_identifier, role)
    return jsonify({"token": token}), 200

@userBluePrint.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    phone_number = data.get("phone_number")
    
    if not all([name, email, password, role, phone_number]):
        return jsonify({"message": "Missing required fields"}), 400
    
    user_id = User.create_user(name, email, password, role, phone_number)
    return jsonify({"message": "User Registered successfully", "user_id": str(user_id)}), 201

@userBluePrint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    user = User.collection.find_one({"email": email})
    if not user or user["password"] != password:
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = Config.generate_jwt(str(user["_id"]), user["role"])
    return jsonify({"token": token}), 200
