from flask import Blueprint, jsonify, request
from models import Booking
from config import token_required
from bson import ObjectId

bookingBluePrint = Blueprint('booking', __name__)

@bookingBluePrint.route('/bookings', methods=['GET'])
def get_all_bookings():
    bookings = []
    for booking in Booking.collection.find():
        bookings.append({
            'id': str(booking['_id']),
            'customer_id': booking['customer_id'],
            'unit_id': booking['unit_id'],
            'check_in_date': booking['check_in_date'],
            'check_out_date': booking['check_out_date'],
            'status': booking['status'],
            'total_price': booking['total_price']
        })
    return jsonify(bookings), 200

@bookingBluePrint.route('/booking/<string:booking_id>', methods=['GET'])
def get_booking_by_id(booking_id):
    booking = Booking.collection.find_one({"_id": ObjectId(booking_id)})

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    return jsonify({
        'id': str(booking['_id']),
        'customer_id': booking['customer_id'],
        'unit_id': booking['unit_id'],
        'check_in_date': booking['check_in_date'],
        'check_out_date': booking['check_out_date'],
        'status': booking['status'],
        'total_price': booking['total_price']
    }), 200

@bookingBluePrint.route('/booking', methods=['POST'])
@token_required
def create_booking(current_user):
    data = request.json

    if not data or 'customer_id' not in data or 'unit_id' not in data or 'check_in_date' not in data or 'check_out_date' not in data or 'status' not in data or 'total_price' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_booking = {
        "customer_id": data['customer_id'],
        "unit_id": data['unit_id'],
        "check_in_date": data['check_in_date'],
        "check_out_date": data['check_out_date'],
        "status": data['status'],
        "total_price": data['total_price']
    }

    result = Booking.collection.insert_one(new_booking)
    return jsonify({"message": "Booking created", "id": str(result.inserted_id)}), 201

@bookingBluePrint.route('/booking/<string:booking_id>', methods=['PUT', 'PATCH'])
@token_required
def update_booking(current_user, booking_id):
    data = request.json

    if not data:
        return jsonify({"message": "No update data provided"}), 400

    updated_booking = Booking.collection.find_one_and_update(
        {"_id": ObjectId(booking_id)},
        {"$set": data},
        return_document=True
    )

    if not updated_booking:
        return jsonify({"message": "Booking not found"}), 404

    return jsonify({"message": "Booking updated successfully"}), 200

@bookingBluePrint.route('/booking/<string:booking_id>', methods=['DELETE'])
@token_required
def delete_booking(current_user, booking_id):
    deleted_booking = Booking.collection.find_one_and_delete({"_id": ObjectId(booking_id)})

    if not deleted_booking:
        return jsonify({"message": "Booking not found"}), 404

    return jsonify({"message": "Booking deleted successfully"}), 200
