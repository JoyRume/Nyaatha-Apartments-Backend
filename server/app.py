from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from user import userBluePrint
from property import propertyBluePrint
from unit import unitBluePrint
from payment import paymentBluePrint
from review import reviewBluePrint
from booking import bookingBluePrint
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Nyaatha_db" 
    mongo = PyMongo(app)
    app.register_blueprint(userBluePrint, url_prefix='/api')
    app.register_blueprint(propertyBluePrint, url_prefix='/api')
    app.register_blueprint(unitBluePrint, url_prefix='/api')
    app.register_blueprint(bookingBluePrint, url_prefix='/api')
    app.register_blueprint(paymentBluePrint, url_prefix='/api')
    app.register_blueprint(reviewBluePrint, url_prefix='/api')
    app.mongo = mongo

    return app

app = create_app()

@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!", 200

if __name__ == '__main__':
    app.run(debug=True)
