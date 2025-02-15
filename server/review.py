from flask import Blueprint, request, jsonify
from bson import ObjectId, errors
from config import token_required
from models import Review

reviewBluePrint = Blueprint('review', __name__)

# Get all reviews
@reviewBluePrint.route("/reviews", methods=["GET"])
@token_required
def get_reviews():
    reviews = Review.collection.find()
    review_list = [{"_id": str(review["_id"]), **review} for review in reviews]
    return jsonify(review_list), 200

# Get review by ID
@reviewBluePrint.route("/reviews/<review_id>", methods=["GET"])
@token_required
def get_review_by_id(review_id):
    try:
        review_obj_id = ObjectId(str(review_id))  
        review = Review.collection.find_one({"_id": review_obj_id})
        if not review:
            return jsonify({"message": "Review not found"}), 404
        review["_id"] = str(review["_id"])
        return jsonify(review), 200
    except errors.InvalidId:
        return jsonify({"message": "Invalid review ID format"}), 400

# Create a review
@reviewBluePrint.route("/reviews", methods=["POST"])
@token_required
def create_review():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    try:
        review_id = Review.collection.insert_one({
            "customer_id": str(data["customer_id"]),
            "unit_id": str(data["unit_id"]),
            "rating": data["rating"],
            "review": data["review"],
            "created_at": data.get("created_at")
        }).inserted_id
        
        return jsonify({"message": "Review created", "review_id": str(review_id)}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update review
@reviewBluePrint.route("/reviews/<review_id>", methods=["PUT", "PATCH"])
@token_required
def update_review(review_id):
    try:
        review_obj_id = ObjectId(str(review_id))  
    except errors.InvalidId:
        return jsonify({"message": "Invalid review ID format"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = Review.collection.update_one({"_id": review_obj_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Review not found"}), 404
    return jsonify({"message": "Review updated"}), 200

# Delete review
@reviewBluePrint.route("/reviews/<review_id>", methods=["DELETE"])
@token_required
def delete_review(review_id):
    try:
        review_obj_id = ObjectId(str(review_id))
    except errors.InvalidId:
        return jsonify({"message": "Invalid review ID format"}), 400

    result = Review.collection.delete_one({"_id": review_obj_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Review not found"}), 404
    return jsonify({"message": "Review deleted"}), 200
