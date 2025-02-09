from pymongo import MongoClient
import enum
from datetime import datetime

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
    
class User:
    collection = db["users"]
    
    @staticmethod
    def create_user(name, email, password, role, phone_number):
        user = {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "phone_number": phone_number
        }
        return User.collection.insert_one(user).inserted_id
    
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
        return Property.collection.insert_one(property_data).inserted_id

class Unit:
    collection = db["units"]

    @staticmethod
    def create_unit(property_id, name, image, unit_type, rental_type, status, price_per_night=None, monthly_rent=None):
        if isinstance(rental_type, str):
            rental_type = RentalType(rental_type)  

        unit = {
            "property_id": property_id,
            "name": name,
            "image": image,
            "type": unit_type,
            "rental_type": rental_type.value,  
            "status": status,
            "price_per_night": price_per_night,
            "monthly_rent": monthly_rent
        }
        return Unit.collection.insert_one(unit).inserted_id


class Booking:
    collection = db["bookings"]

    @staticmethod
    def create_booking(customer_id, unit_id, check_in_date, check_out_date, status, total_price):
        booking = {
            "customer_id": customer_id,
            "unit_id": unit_id,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "status": status.value,
            "total_price": total_price
        }
        return Booking.collection.insert_one(booking).inserted_id

class Payment:
    collection = db["payments"]

    @staticmethod
    def create_payment(booking_id, amount, payment_method, status, transaction_reference):
        payment = {
            "booking_id": booking_id,
            "amount": amount,
            "payment_method": payment_method.value,
            "status": status.value,
            "transaction_reference": transaction_reference
        }
        return Payment.collection.insert_one(payment).inserted_id

class Review:
    collection = db["reviews"]

    @staticmethod
    def create_review(customer_id, unit_id, rating, review):
        review_data = {
            "customer_id": customer_id,
            "unit_id": unit_id,
            "rating": rating,
            "review": review,
            "created_at": datetime.utcnow()
        }
        return Review.collection.insert_one(review_data).inserted_id