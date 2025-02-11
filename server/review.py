from flask import Blueprint, jsonify, request
from models import Review
from config import token_required
from bson import ObjectId
from datetime import datetime

reviewBluePrint = Blueprint('review', __name__)

@reviewBluePrint.route('/reviews', methods=['GET'])
def get_all_reviews():
    reviews = []
    for review in Review.collection.find():
        reviews.append({
            'id': str(review['_id']),
            'customer_id': review['customer_id'],
            'unit_id': review['unit_id'],
            'rating': review['rating'],
            'review': review['review'],
            'created_at': review['created_at']
        })
    return jsonify(reviews), 200

@reviewBluePrint.route('/review/<string:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review = Review.collection.find_one({"_id": ObjectId(review_id)})

    if not review:
        return jsonify({"message": "Review not found"}), 404

    return jsonify({
        'id': str(review['_id']),
        'customer_id': review['customer_id'],
        'unit_id': review['unit_id'],
        'rating': review['rating'],
        'review': review['review'],
        'created_at': review['created_at']
    }), 200

@reviewBluePrint.route('/review', methods=['POST'])
@token_required
def create_review(current_user):
    data = request.json

    if not data or 'customer_id' not in data or 'unit_id' not in data or 'rating' not in data or 'review' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_review = {
        "customer_id": data['customer_id'],
        "unit_id": data['unit_id'],
        "rating": data['rating'],
        "review": data['review'],
        "created_at": datetime.utcnow()
    }

    result = Review.collection.insert_one(new_review)
    return jsonify({"message": "Review created", "id": str(result.inserted_id)}), 201
