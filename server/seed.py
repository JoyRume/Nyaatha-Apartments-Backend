from pymongo import MongoClient
from models import User, UserRole, Property, RentalType, Unit, Booking, PaymentMethod, PaymentStatus, BookingStatus, Review, Payment

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Nyaatha_db"]

# Insert 5 Users
User.create_user("Alice Johnson", "alice.johnson@gmail.com", "password123", UserRole.Customer, "0701122334")
User.create_user("Bob Smith", "bob.smith@gmail.com", "password456", UserRole.Tenant, "0702233445")
User.create_user("Charlie Brown", "charlie.brown@gmail.com", "password789", UserRole.Admin, "0703344556")
User.create_user("Diana White", "diana.white@gmail.com", "password101112", UserRole.Customer, "0704455667")
User.create_user("Eve Davis", "eve.davis@gmail.com", "password131415", UserRole.Tenant, "0705566778")

# Insert 5 Properties
Property.create_property("Green Valley", "Nairobi, Kenya", "https://unsplash.com/photos/white-and-grey-concrete-building-near-swimming-pool-under-clear-sky-during-daytime-2d4lAQAlbDA", RentalType.ShortTerm, "A beautiful garden view villa.")
Property.create_property("Blue Ridge", "Mombasa, Kenya", "https://unsplash.com/photos/brown-and-white-wooden-house-near-green-trees-during-daytime-2gDwlIim3Uw", RentalType.Commercial, "A spacious office space ideal for businesses.")
Property.create_property("Mountain Peak", "Nakuru, Kenya", "https://unsplash.com/photos/brown-and-white-concrete-building-MAnVoJlQUvg", RentalType.ShortTerm, "A cozy mountain cabin for vacations.")
Property.create_property("Sunset Tower", "Nairobi, Kenya", "https://unsplash.com/photos/brown-and-black-concrete-building-JvQ0Q5IkeMM", RentalType.Commercial, "A modern skyscraper with luxurious office spaces.")
Property.create_property("Seaside Escape", "Mombasa, Kenya", "https://unsplash.com/photos/white-and-brown-concrete-building-bfOQSDwEFg4", RentalType.ShortTerm, "A beach house with stunning views.")

property_ids = [1, 2, 3, 4, 5]

# Insert Units
Unit.create_unit(property_ids[0], "Unit A", "https://images.unsplash.com/photo-1514779324364-8400d49e81de?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDF8fHxlbnwwfHx8fHw%3D", "Mansion",RentalType.ShortTerm, "Available", 0, 10000)
Unit.create_unit(property_ids[1], "Unit B", "https://images.unsplash.com/photo-1543748984-8ffa30d42668?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDEzfHx8ZW58MHx8fHx8", "Bungalow", RentalType.Commercial, "Available", 0, 10000)
Unit.create_unit(property_ids[2], "Unit C", "https://images.unsplash.com/photo-1708570319822-5789229071f7?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDI2fHx8ZW58MHx8fHx8", "Mansionnate", RentalType.ShortTerm, "Booked", 4000)

Unit.create_unit(property_ids[3], "Unit D", "https://images.unsplash.com/photo-1664484841762-c4ddb05159ab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDQ2fHx8ZW58MHx8fHx8", "Single", RentalType.Commercial, "Available", 0, 12000)

Unit.create_unit(property_ids[4], "Unit E", "https://images.unsplash.com/photo-1735514326714-ae7d43827886?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDU4fHx8ZW58MHx8fHx8", "BedSitter", RentalType.ShortTerm, "Booked",10, 8000)

# Insert bookings, payments, and reviews
booking_ids = []
for i in range(1, 6):
    booking_ids.append(Booking.create_booking(i, 1, "2025-02-01", "2025-02-05", BookingStatus.Confirmed, 5000))

for i in range(1, 6):
    Payment.create_payment(booking_ids[i-1], 5000, PaymentMethod.Mpesa, PaymentStatus.Completed, f"TXN{i}")

for i in range(1, 6):
    Review.create_review(i, 1, 5, "Excellent service and great place to stay!")
