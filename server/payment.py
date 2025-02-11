from flask import Blueprint, jsonify, request
from models import Payment
from config import token_required
from bson import ObjectId

paymentBluePrint = Blueprint('payment', __name__)

@paymentBluePrint.route('/payments', methods=['GET'])
def get_all_payments():
    payments = []
    for payment in Payment.collection.find():
        payments.append({
            'id': str(payment['_id']),
            'booking_id': payment['booking_id'],
            'amount': payment['amount'],
            'payment_method': payment['payment_method'],
            'status': payment['status'],
            'transaction_reference': payment['transaction_reference']
        })
    return jsonify(payments), 200

@paymentBluePrint.route('/payment/<string:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    payment = Payment.collection.find_one({"_id": ObjectId(payment_id)})

    if not payment:
        return jsonify({"message": "Payment not found"}), 404

    return jsonify({
        'id': str(payment['_id']),
        'booking_id': payment['booking_id'],
        'amount': payment['amount'],
        'payment_method': payment['payment_method'],
        'status': payment['status'],
        'transaction_reference': payment['transaction_reference']
    }), 200

@paymentBluePrint.route('/payment', methods=['POST'])
@token_required
def create_payment(current_user):
    data = request.json

    if not data or 'booking_id' not in data or 'amount' not in data or 'payment_method' not in data or 'status' not in data or 'transaction_reference' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_payment = {
        "booking_id": data['booking_id'],
        "amount": data['amount'],
        "payment_method": data['payment_method'],
        "status": data['status'],
        "transaction_reference": data['transaction_reference']
    }

    result = Payment.collection.insert_one(new_payment)
    return jsonify({"message": "Payment created", "id": str(result.inserted_id)}), 201

@paymentBluePrint.route('/payment/<string:payment_id>', methods=['PUT', 'PATCH'])
@token_required
def update_payment(current_user, payment_id):
    data = request.json

    if not data:
        return jsonify({"message": "No update data provided"}), 400

    updated_payment = Payment.collection.find_one_and_update(
        {"_id": ObjectId(payment_id)},
        {"$set": data},
        return_document=True
    )

    if not updated_payment:
        return jsonify({"message": "Payment not found"}), 404

    return jsonify({"message": "Payment updated successfully"}), 200

@paymentBluePrint.route('/payment/<string:payment_id>', methods=['DELETE'])
@token_required
def delete_payment(current_user, payment_id):
    deleted_payment = Payment.collection.find_one_and_delete({"_id": ObjectId(payment_id)})

    if not deleted_payment:
        return jsonify({"message": "Payment not found"}), 404

    return jsonify({"message": "Payment deleted successfully"}), 200
