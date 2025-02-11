from flask import Blueprint, jsonify, request, current_app
from models import User

userBluePrint = Blueprint('user', __name__)

@userBluePrint.route('/users', methods=['GET'])
def get_all_users():
    users = current_app.mongo.db.users.find()  
    
    user_list = []
    for user in users:
        user_list.append({
            'id': str(user['_id']),  
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'phone_number': user['phone_number']
        })
    return jsonify(user_list), 200



