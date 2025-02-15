from flask import Blueprint, request, jsonify
from bson import ObjectId, errors
from config import token_required
from models import Booking

bookingBluePrint = Blueprint('booking', __name__)

# Get all bookings
@bookingBluePrint.route("/bookings", methods=["GET"])
@token_required
def get_bookings():
    bookings = Booking.collection.find()
    booking_list = [{"_id": str(booking["_id"]), **booking} for booking in bookings]
    return jsonify(booking_list), 200

# Get booking by ID
@bookingBluePrint.route("/bookings/<booking_id>", methods=["GET"])
@token_required
def get_booking_by_id(booking_id):
    try:
        booking_obj_id = ObjectId(str(booking_id))  
        booking = Booking.collection.find_one({"_id": booking_obj_id})
        if not booking:
            return jsonify({"message": "Booking not found"}), 404
        booking["_id"] = str(booking["_id"])
        return jsonify(booking), 200
    except errors.InvalidId:
        return jsonify({"message": "Invalid booking ID format"}), 400

# Create a booking
@bookingBluePrint.route("/bookings", methods=["POST"])
@token_required
def create_booking():
    data = request.get_json()
    current_user = request.user["user_id"]

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        booking_id = Booking.create_booking(
            customer_id=str(current_user),  
            unit_id=str(data["unit_id"]),
            check_in_date=data["check_in_date"],
            check_out_date=data["check_out_date"],
            status=data.get("status", "Pending"),
            total_price=data["total_price"]
        )
        return jsonify({"message": "Booking created", "booking_id": booking_id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@bookingBluePrint.route("/bookings/<booking_id>", methods=["PUT"])
@token_required
def update_booking(booking_id):
    try:
        booking_obj_id = ObjectId(str(booking_id))  
    except errors.InvalidId:
        return jsonify({"message": "Invalid booking ID format"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = Booking.collection.update_one({"_id": booking_obj_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Booking not found"}), 404
    return jsonify({"message": "Booking updated"}), 200

@bookingBluePrint.route("/bookings/<booking_id>", methods=["PATCH"])
@token_required
def patch_booking(booking_id):
    try:
        booking_obj_id = ObjectId(str(booking_id))
    except errors.InvalidId:
        return jsonify({"message": "Invalid booking ID format"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = Booking.collection.update_one({"_id": booking_obj_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Booking not found"}), 404
    return jsonify({"message": "Booking updated"}), 200

@bookingBluePrint.route("/bookings/<booking_id>", methods=["DELETE"])
@token_required
def delete_booking(booking_id):
    try:
        booking_obj_id = ObjectId(str(booking_id))
    except errors.InvalidId:
        return jsonify({"message": "Invalid booking ID format"}), 400

    result = Booking.collection.delete_one({"_id": booking_obj_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Booking not found"}), 404
    return jsonify({"message": "Booking deleted"}), 200
