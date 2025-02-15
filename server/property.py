from flask import Blueprint, jsonify, request
from models import Property
from config import token_required
from bson import ObjectId, errors

propertyBluePrint = Blueprint('property', __name__)

# Get all properties
@propertyBluePrint.route('/properties', methods=['GET'])
@token_required
def get_all_properties():
    properties = Property.collection.find()
    property_list = [{"_id": str(p["_id"]), **p} for p in properties]
    return jsonify(property_list), 200

# Get property by ID
@propertyBluePrint.route('/properties/<property_id>', methods=['GET'])
@token_required
def get_property_by_id(property_id):
    try:
        property_obj_id = ObjectId(property_id)
        property_data = Property.collection.find_one({"_id": property_obj_id})
        if not property_data:
            return jsonify({"message": "Property not found"}), 404
        property_data["_id"] = str(property_data["_id"])
        return jsonify(property_data), 200
    except errors.InvalidId:
        return jsonify({"message": "Invalid property ID format"}), 400

# Create a property
@propertyBluePrint.route('/properties', methods=['POST'])
@token_required
def create_property():
    data = request.get_json()
    
    if not data or 'name' not in data or 'location' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    try:
        property_id = Property.collection.insert_one({
            "name": data["name"],
            "location": data["location"],
            "image": data.get("image", ""),
            "rental_type": data.get("rental_type", ""),
            "description": data.get("description", "")
        }).inserted_id
        
        return jsonify({"message": "Property created", "property_id": str(property_id)}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update property
@propertyBluePrint.route('/properties/<property_id>', methods=['PUT', 'PATCH'])
@token_required
def update_property(property_id):
    try:
        property_obj_id = ObjectId(property_id)
    except errors.InvalidId:
        return jsonify({"message": "Invalid property ID format"}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "No update data provided"}), 400
    
    result = Property.collection.update_one({"_id": property_obj_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Property not found"}), 404
    
    return jsonify({"message": "Property updated successfully"}), 200

# Delete property
@propertyBluePrint.route('/properties/<property_id>', methods=['DELETE'])
@token_required
def delete_property(property_id):
    try:
        property_obj_id = ObjectId(property_id)
    except errors.InvalidId:
        return jsonify({"message": "Invalid property ID format"}), 400
    
    result = Property.collection.delete_one({"_id": property_obj_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Property not found"}), 404
    
    return jsonify({"message": "Property deleted successfully"}), 200
