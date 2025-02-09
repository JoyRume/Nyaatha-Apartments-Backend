from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from user import userBluePrint

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Nyaatha_db" 
    mongo = PyMongo(app)
    app.register_blueprint(userBluePrint, url_prefix='/api')
    app.mongo = mongo

    return app

app = create_app()

@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!", 200

if __name__ == '__main__':
    app.run(debug=True)
