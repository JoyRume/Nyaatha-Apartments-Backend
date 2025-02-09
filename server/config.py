import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

SECRET_KEY = ""

def generate_jwt(user_identifier):
    token = jwt.encode({
        "sub": user_identifier,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")
    
    print(f"Generated JWT Token: {token}")
    return token

def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"Decoded JWT Token: {decoded_token}")
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token has expired!")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token!")
        return None

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            print("Token is missing!")
            return jsonify({"message": "Token is missing!"}), 403
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        print(f"Received JWT Token: {token}")
        
        decoded_token = decode_jwt(token)
        
        if decoded_token is None:
            print("Token is invalid or expired!")
            return jsonify({"message": "Token is invalid or expired!"}), 403
        
        current_user = decoded_token["sub"]
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function
