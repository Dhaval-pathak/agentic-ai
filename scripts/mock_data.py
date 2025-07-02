import pymongo
from datetime import datetime, timedelta
from bson import ObjectId

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["multi_agent"]

# Clear existing collections
db.clients.drop()
db.orders.drop()
db.payments.drop()
db.courses.drop()
db.classes.drop()

# Mock data for clients
clients = [
    {
        "_id": ObjectId(),
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "phone": "+919876543210",
        "enrolled_services": ["Yoga Beginner", "Pilates"],
        "status": "active"
    },
    {
        "_id": ObjectId(),
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+919876543211",
        "enrolled_services": ["Yoga Advanced"],
        "status": "inactive"
    }
]

# Mock data for orders
orders = [
    {
        "_id": ObjectId("1234567890abcdef12345678"),
        "client_id": clients[0]["_id"],
        "course_id": ObjectId("1234567890abcdef12345601"),
        "status": "paid",
        "amount": 5000,
        "order_date": datetime.now() - timedelta(days=5)
    },
    {
        "_id": ObjectId("1234567890abcdef12345679"),
        "client_id": clients[1]["_id"],
        "course_id": ObjectId("1234567890abcdef12345602"),
        "status": "pending",
        "amount": 6000,
        "order_date": datetime.now() - timedelta(days=2)
    }
]

# Mock data for payments
payments = [
    {
        "_id": ObjectId(),
        "order_id": orders[0]["_id"],
        "client_id": clients[0]["_id"],
        "amount": 5000,
        "payment_date": datetime.now() - timedelta(days=4),
        "status": "completed"
    },
    {
        "_id": ObjectId(),
        "order_id": orders[1]["_id"],
        "client_id": clients[1]["_id"],
        "amount": 3000,
        "payment_date": datetime.now() - timedelta(days=1),
        "status": "partial"
    }
]

# Mock data for courses
courses = [
    {
        "_id": ObjectId("1234567890abcdef12345601"),
        "name": "Yoga Beginner",
        "instructor": "Amit Patel",
        "duration": "4 weeks",
        "price": 5000,
        "status": "active"
    },
    {
        "_id": ObjectId("1234567890abcdef12345602"),
        "name": "Pilates",
        "instructor": "Sarah Lee",
        "duration": "6 weeks",
        "price": 6000,
        "status": "active"
    }
]

# Mock data for classes
classes = [
    {
        "_id": ObjectId(),
        "course_id": courses[0]["_id"],
        "name": "Yoga Beginner - Session 1",
        "instructor": "Amit Patel",
        "date": datetime.now() + timedelta(days=1),
        "status": "scheduled",
        "attendees": [clients[0]["_id"]]
    },
    {
        "_id": ObjectId(),
        "course_id": courses[1]["_id"],
        "name": "Pilates - Session 1",
        "instructor": "Sarah Lee",
        "date": datetime.now() + timedelta(days=3),
        "status": "scheduled",
        "attendees": [clients[0]["_id"], clients[1]["_id"]]
    }
]

# Insert mock data into collections
db.clients.insert_many(clients)
db.orders.insert_many(orders)
db.payments.insert_many(payments)
db.courses.insert_many(courses)
db.classes.insert_many(classes)

print("Mock data inserted successfully!")
client.close()