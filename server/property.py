from flask import Blueprint,jsonify, request
from models import Property
from config import token_required
from bson import ObjectId

propertyBluePrint = Blueprint('property', __name__)

@propertyBluePrint.route('/properties', methods=['GET'])
def get_all_properties():
    property_list = []
    for property in Property.collection.find():
        property_list.append({
            'id': str(property['_id']),
            'name': property['name'],
            'location': property['location'],
            'image': property['image'],
            'rental_type': property['rental_type'],
            'description': property['description']
        })
    return jsonify(property_list), 200

@propertyBluePrint.route('/property/<string:property_id>', methods=['GET'])
def get_property_by_id(property_id):
    property_data = Property.collection.find_one({"_id": ObjectId(property_id)})
    if not property_data:
        return jsonify({"message": "Property not found"}), 404
    
    property_details = {
        'id':str(property_data['_id']),
        'name':property_data['name'],
        'location':property_data['location'],
        'image':property_data['image'],
        'rental_type':property_data['rental_type'],
        'description':property_data['description']
    }
    return jsonify(property_details), 200

@propertyBluePrint.route('/property', methods=['POST'])
def create_property(current_user):
    data = request.json
    if not data or 'name'not in data or 'location' not in data:
        return jsonify({"message": "Missing the required fields"}), 400
    new_property = {
        "name": data['name'],
        "location": data['location'],
        "image": data.get('image', ''),
        "rental_type": data.get('rental_type', ''),
        "description": data.get('description', '')
    }
    result = Property.collection.insert_one(new_property)
    return jsonify({"message": "Property created", "id": str(result.inserted_id)}), 201

@propertyBluePrint.route('/property/<string:property_id>', methods=['PUT'])
@token_required
def update_property(current_user, property_id):
    data = request.json

    if not data:
        return jsonify({"message": "No update data provided"}), 400

    updated_property = Property.collection.find_one_and_update(
        {"_id": ObjectId(property_id)},
        {"$set": data},
        return_document=True
    )

    if not updated_property:
        return jsonify({"message": "Property not found"}), 404

    return jsonify({"message": "Property updated successfully"}), 200

@propertyBluePrint.route('/property/<string:property_id>', methods=['PATCH'])
@token_required
def patch_property(property_id):
    data = request.json

    if not data:
        return jsonify({"message": "No update data provided"}), 400

    updated_property = Property.collection.find_one_and_update(
        {"_id": ObjectId(property_id)},
        {"$set": data},
        return_document=True
    )

    if not updated_property:
        return jsonify({"message": "Property not found"}), 404

    return jsonify({"message": "Property patched successfully"}), 200

@propertyBluePrint.route('/property/<string:property_id>', methods=['DELETE'])
@token_required
def delete_property(current_user, property_id):
    deleted_property = Property.collection.find_one_and_delete({"_id": ObjectId(property_id)})

    if not deleted_property:
        return jsonify({"message": "Property not found"}), 404

    return jsonify({"message": "Property deleted successfully"}), 200

