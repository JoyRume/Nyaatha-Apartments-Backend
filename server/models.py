from pymongo import MongoClient
from bson import ObjectId
import enum
import bcrypt
from datetime import datetime
from bson.errors import InvalidId


# Database Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Nyaatha_db"]

class UserRole(str, enum.Enum):
    Admin = "Admin"
    Customer = "Customer"
    Tenant = "Tenant"

class RentalType(str, enum.Enum):
    ShortTerm = "Short-term"
    Commercial = "Commercial"
    
class BookingStatus(str, enum.Enum):
    Pending = "Pending"
    Confirmed = "Confirmed"
    Declined = "Declined"
    Cancelled = "Cancelled"
    Completed = "Completed"

class PaymentMethod(str, enum.Enum):
    Mpesa = "M-Pesa"
    CreditCard = "CreditCard"
    BankTransfer = "BankTransfer"
    
class PaymentStatus(str, enum.Enum):
    Pending = "Pending"
    Confirmed = "Confirmed"
    Completed = "Completed"
    Failed = "Failed"

# User Model
class User:
    collection = db["users"]

    @staticmethod
    def create_user(name, email, password, role, phone_number):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
            "phone_number": phone_number
        }
        return str(User.collection.insert_one(user).inserted_id)  

    @staticmethod
    def get_user_by_id(user_id):
        user = User.collection.find_one({"_id": str(ObjectId(user_id))})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None

    @staticmethod
    def get_user_by_email(email):
        user = User.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

# Property Model
class Property:
    collection = db["properties"]

    @staticmethod
    def create_property(name, location, image, rental_type, description):
        property_data = {
            "name": name,
            "location": location,
            "image": image,
            "rental_type": rental_type,
            "description": description
        }
        return str(Property.collection.insert_one(property_data).inserted_id)

# Unit Model
class Unit:
    collection = db["units"]

    @staticmethod
    def create_unit(property_id, name, image, unit_type, rental_type, status, price_per_night=None, monthly_rent=None):
        if isinstance(rental_type, str):
            rental_type = RentalType(rental_type)  

        unit = {
            "property_id": str(ObjectId(property_id)),
            "name": name,
            "image": image,
            "type": unit_type,
            "rental_type": rental_type.value,  
            "status": status,
            "price_per_night": price_per_night,
            "monthly_rent": monthly_rent
        }
        return str(Unit.collection.insert_one(unit).inserted_id)

class Booking:
    collection = db["bookings"]

    @staticmethod
    def create_booking(customer_id, unit_id, check_in_date, check_out_date, status, total_price):
        try:
            booking = {
                "customer_id": str(ObjectId(customer_id)),
                "unit_id": str(ObjectId(unit_id)),
                "check_in_date": datetime.strptime(check_in_date, "%Y-%m-%d"),
                "check_out_date": datetime.strptime(check_out_date, "%Y-%m-%d"),
                "status": status,
                "total_price": total_price
            }
            return str(Booking.collection.insert_one(booking).inserted_id)
        except InvalidId:
            raise ValueError("Invalid customer_id or unit_id format")


# Payment Model
class Payment:
    collection = db["payments"]

    @staticmethod
    def create_payment(booking_id, amount, payment_method, status, transaction_reference):
        if isinstance(payment_method, str):
            payment_method = PaymentMethod(payment_method)

        if isinstance(status, str):
            status = PaymentStatus(status)

        payment = {
            "booking_id": str(ObjectId(booking_id)),
            "amount": amount,
            "payment_method": payment_method.value,
            "status": status.value,
            "transaction_reference": transaction_reference
        }
        return str(Payment.collection.insert_one(payment).inserted_id)

# Review Model
class Review:
    collection = db["reviews"]

    @staticmethod
    def create_review(customer_id, unit_id, rating, review):
        review_data = {
            "customer_id": str(ObjectId(customer_id)),
            "unit_id": str(ObjectId(unit_id)),
            "rating": rating,
            "review": review,
            "created_at": datetime.utcnow()
        }
        return str(Review.collection.insert_one(review_data).inserted_id)
