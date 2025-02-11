from flask import Blueprint, jsonify, request
from models import Unit
from config import token_required
from bson import ObjectId

unitBluePrint = Blueprint('unit', __name__)

@unitBluePrint.route('/units', methods=['GET'])
def get_all_units():
    units = []
    for unit in Unit.collection.find():
        units.append({
            'id': str(unit['_id']),
            'property_id': unit['property_id'],
            'name': unit['name'],
            'image': unit.get('image', ''),
            'type': unit['type'],
            'rental_type': unit['rental_type'],
            'status': unit['status'],
            'price_per_night': unit.get('price_per_night'),
            'monthly_rent': unit.get('monthly_rent')
        })
    return jsonify(units), 200

@unitBluePrint.route('/unit/<string:unit_id>', methods=['GET'])
def get_unit_by_id(unit_id):
    unit = Unit.collection.find_one({"_id": ObjectId(unit_id)})
    
    if not unit:
        return jsonify({"message": "Unit not found"}), 404

    unit_data = {
        'id': str(unit['_id']),
        'property_id': unit['property_id'],
        'name': unit['name'],
        'image': unit.get('image', ''),
        'type': unit['type'],
        'rental_type': unit['rental_type'],
        'status': unit['status'],
        'price_per_night': unit.get('price_per_night'),
        'monthly_rent': unit.get('monthly_rent')
    }

    return jsonify(unit_data), 200

@unitBluePrint.route('/unit', methods=['POST'])
@token_required
def create_unit(current_user):
    data = request.json

    if not data or 'property_id' not in data or 'name' not in data or 'type' not in data or 'rental_type' not in data or 'status' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_unit = {
        "property_id": data['property_id'],
        "name": data['name'],
        "image": data.get('image', ''),
        "type": data['type'],
        "rental_type": data['rental_type'],
        "status": data['status'],
        "price_per_night": data.get('price_per_night'),
        "monthly_rent": data.get('monthly_rent')
    }

    result = Unit.collection.insert_one(new_unit)
    return jsonify({"message": "Unit created", "id": str(result.inserted_id)}), 201

@unitBluePrint.route('/unit/<string:unit_id>', methods=['PUT'])
@token_required
def update_unit(current_user, unit_id):
    data = request.json

    if not data:
        return jsonify({"message": "No update data provided"}), 400

    updated_unit = Unit.collection.find_one_and_update(
        {"_id": ObjectId(unit_id)},
        {"$set": data},
        return_document=True
    )

    if not updated_unit:
        return jsonify({"message": "Unit not found"}), 404

    return jsonify({"message": "Unit updated successfully"}), 200

@unitBluePrint.route('/unit/<string:unit_id>', methods=['PATCH'])
@token_required
def patch_unit(current_user, unit_id):
    data = request.json

    if not data:
        return jsonify({"message": "No update data provided"}), 400

    updated_unit = Unit.collection.find_one_and_update(
        {"_id": ObjectId(unit_id)},
        {"$set": data},
        return_document=True
    )

    if not updated_unit:
        return jsonify({"message": "Unit not found"}), 404

    return jsonify({"message": "Unit patched successfully"}), 200

@unitBluePrint.route('/unit/<string:unit_id>', methods=['DELETE'])
@token_required
def delete_unit(current_user, unit_id):
    deleted_unit = Unit.collection.find_one_and_delete({"_id": ObjectId(unit_id)})

    if not deleted_unit:
        return jsonify({"message": "Unit not found"}), 404

    return jsonify({"message": "Unit deleted successfully"}), 200
