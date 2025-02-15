from flask import Blueprint, request, jsonify
from bson import ObjectId, errors
from config import token_required
from models import Unit

unitBluePrint = Blueprint('unit', __name__)

# Get all units
@unitBluePrint.route("/units", methods=["GET"])
@token_required
def get_all_units():
    units = Unit.collection.find()
    unit_list = [{"_id": str(unit["_id"]), **unit} for unit in units]
    return jsonify(unit_list), 200

# Get unit by ID
@unitBluePrint.route("/units/<unit_id>", methods=["GET"])
@token_required
def get_unit_by_id(unit_id):
    try:
        unit_obj_id = ObjectId(str(unit_id))  
        unit = Unit.collection.find_one({"_id": unit_obj_id})
        if not unit:
            return jsonify({"message": "Unit not found"}), 404
        unit["_id"] = str(unit["_id"])
        return jsonify(unit), 200
    except errors.InvalidId:
        return jsonify({"message": "Invalid unit ID format"}), 400

# Create a unit
@unitBluePrint.route("/units", methods=["POST"])
@token_required
def create_unit():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        unit_id = Unit.collection.insert_one(data).inserted_id
        return jsonify({"message": "Unit created", "unit_id": str(unit_id)}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update unit
@unitBluePrint.route("/units/<unit_id>", methods=["PUT", "PATCH"])
@token_required
def update_unit(unit_id):
    try:
        unit_obj_id = ObjectId(str(unit_id))  
    except errors.InvalidId:
        return jsonify({"message": "Invalid unit ID format"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = Unit.collection.update_one({"_id": unit_obj_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Unit not found"}), 404
    return jsonify({"message": "Unit updated"}), 200

# Delete unit
@unitBluePrint.route("/units/<unit_id>", methods=["DELETE"])
@token_required
def delete_unit(unit_id):
    try:
        unit_obj_id = ObjectId(str(unit_id))
    except errors.InvalidId:
        return jsonify({"message": "Invalid unit ID format"}), 400

    result = Unit.collection.delete_one({"_id": unit_obj_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Unit not found"}), 404
    return jsonify({"message": "Unit deleted"}), 200
