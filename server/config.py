# import secrets
import os
import jwt
import datetime
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    @staticmethod
    def generate_jwt(user_identifier, role):
        token = jwt.encode({
            "sub": user_identifier,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }, Config.SECRET_KEY, algorithm="HS256")
        return token

# Middleware to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]  # Fix split error
            except IndexError:
                return jsonify({"message": "Invalid token format"}), 401

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user = {"user_id": data["sub"], "role": data.get("role")}
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

# Restricting access by role
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(request, "user"):
                return jsonify({"message": "Token verification failed"}), 401

            if request.user["role"] != required_role:
                return jsonify({"message": "Unauthorized: Insufficient permissions"}), 403

            return f(*args, **kwargs)

        return wrapper
    return decorator

# secret_key = secrets.token_hex(32)
# print("Secret key:", secret_key)