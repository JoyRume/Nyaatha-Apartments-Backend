from flask import Blueprint, request, jsonify
from bson import ObjectId, errors
from config import token_required
from models import Payment

paymentBluePrint = Blueprint('payment', __name__)

# Get all payments
@paymentBluePrint.route("/payments", methods=["GET"])
@token_required
def get_payments():
    payments = Payment.collection.find()
    payment_list = [{"_id": str(payment["_id"]), **payment} for payment in payments]
    return jsonify(payment_list), 200

# Get payment by ID
@paymentBluePrint.route("/payments/<payment_id>", methods=["GET"])
@token_required
def get_payment_by_id(payment_id):
    try:
        payment_obj_id = ObjectId(str(payment_id))  
        payment = Payment.collection.find_one({"_id": payment_obj_id})
        if not payment:
            return jsonify({"message": "Payment not found"}), 404
        payment["_id"] = str(payment["_id"])
        return jsonify(payment), 200
    except errors.InvalidId:
        return jsonify({"message": "Invalid payment ID format"}), 400

# Create a payment
@paymentBluePrint.route("/payments", methods=["POST"])
@token_required
def create_payment():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        payment_id = Payment.create_payment(
            booking_id=str(data["booking_id"]),
            amount=data["amount"],
            payment_method=data["payment_method"],
            status=data.get("status", "Pending"),
            transaction_reference=data["transaction_reference"]  
        )
        return jsonify({"message": "Payment created", "payment_id": payment_id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update payment
@paymentBluePrint.route("/payments/<payment_id>", methods=["PUT", "PATCH"])
@token_required
def update_payment(payment_id):
    try:
        payment_obj_id = ObjectId(str(payment_id))  
    except errors.InvalidId:
        return jsonify({"message": "Invalid payment ID format"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = Payment.collection.update_one({"_id": payment_obj_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Payment not found"}), 404
    return jsonify({"message": "Payment updated"}), 200

# Delete payment
@paymentBluePrint.route("/payments/<payment_id>", methods=["DELETE"])
@token_required
def delete_payment(payment_id):
    try:
        payment_obj_id = ObjectId(str(payment_id))
    except errors.InvalidId:
        return jsonify({"message": "Invalid payment ID format"}), 400

    result = Payment.collection.delete_one({"_id": payment_obj_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Payment not found"}), 404
    return jsonify({"message": "Payment deleted"}), 200
