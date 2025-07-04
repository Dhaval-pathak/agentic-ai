from pymongo import MongoClient
from crewai.tools.base_tool import BaseTool
from pydantic import PrivateAttr
import datetime
from typing import Dict, Any
from bson import ObjectId
import json

class MongoDBTool(BaseTool):
    name: str = "MongoDBTool"
    description: str = """Comprehensive MongoDB tool for client, order, payment, course, and class management.
    Use this tool with properly formatted JSON strings for different actions:
    
    Examples:
    - Find client: '{"action": "find_client", "query": {"email": "priya@example.com"}}'
    - Get upcoming classes: '{"action": "get_upcoming_classes"}'
    - Get order by ID: '{"action": "get_order_by_id", "order_id": "1234567890abcdef12345678"}'
    - Calculate revenue: '{"action": "calculate_revenue", "start_date": "2025-06-01", "end_date": "2025-06-30"}'
    - Get client stats: '{"action": "get_client_stats"}'
    - Get top courses: '{"action": "get_top_courses", "limit": 5}'
    """
    _client: MongoClient = PrivateAttr()
    _db: object = PrivateAttr()

    def __init__(self, uri, db_name, **data):
        super().__init__(**data)
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
        print("Connected to MongoDB:", self._db.list_collection_names())

    def find_client(self, query: Dict[str, Any]):
        """Find client by name, email, or phone"""
        try:
            search_query = {}
            if "name" in query:
                search_query["name"] = {"$regex": query["name"], "$options": "i"}
            if "email" in query:
                search_query["email"] = query["email"]
            if "phone" in query:
                search_query["phone"] = query["phone"]
            
            result = self._db.clients.find_one(search_query, {"_id": 0})
            return result if result else "Client not found"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_client_orders(self, client_email: str):
        """Get all orders for a specific client by email"""
        try:
            client = self._db.clients.find_one({"email": client_email})
            if not client:
                return "Client not found"
            
            orders = list(self._db.orders.find({"client_id": client["_id"]}, {"_id": 0}))
            return orders
        except Exception as e:
            return f"Error: {str(e)}"

    def get_order_by_id(self, order_id: str):
        """Get order details by order ID"""
        try:
            order = self._db.orders.find_one({"_id": ObjectId(order_id)}, {"_id": 0})
            if order:
                # Get client info
                client = self._db.clients.find_one({"_id": order["client_id"]}, {"name": 1, "email": 1})
                if client:
                    order["client_info"] = {"name": client["name"], "email": client["email"]}
            return order if order else "Order not found"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_payment_info(self, order_id: str):
        """Get payment details for an order by order ID"""
        try:
            payments = list(self._db.payments.find({"order_id": ObjectId(order_id)}, {"_id": 0}))
            return payments
        except Exception as e:
            return f"Error: {str(e)}"

    def get_pending_payments(self):
        """Get all pending payments"""
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "orders",
                        "localField": "order_id",
                        "foreignField": "_id",
                        "as": "order_info"
                    }
                },
                {
                    "$match": {
                        "$or": [
                            {"status": "pending"},
                            {"status": "partial"},
                            {"order_info.status": "pending"}
                        ]
                    }
                }
            ]
            result = list(self._db.payments.aggregate(pipeline))
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def get_classes_for_week(self, start_date: str, end_date: str):
        """Get classes for a specific date range"""
        try:
            start_dt = datetime.datetime.fromisoformat(start_date)
            end_dt = datetime.datetime.fromisoformat(end_date)
            
            query = {"date": {"$gte": start_dt, "$lte": end_dt}}
            classes = list(self._db.classes.find(query, {"_id": 0}))
            return classes if classes else "No classes found in the selected date range."
        except Exception as e:
            return f"Error: {str(e)}"

    def get_courses_by_instructor(self, instructor: str):
        """Get courses by instructor name"""
        try:
            courses = list(self._db.courses.find(
                {"instructor": {"$regex": instructor, "$options": "i"}},
                {"_id": 0}
            ))
            return courses
        except Exception as e:
            return f"Error: {str(e)}"

    def get_upcoming_classes(self):
        """Get all upcoming classes"""
        try:
            current_date = datetime.datetime.now()
            classes = list(self._db.classes.find(
                {"date": {"$gte": current_date}},
                {"_id": 0}
            ).sort("date", 1))
            return classes
        except Exception as e:
            return f"Error: {str(e)}"

    def calculate_revenue(self, start_date: str, end_date: str):
        """Calculate revenue for a date range"""
        try:
            start_dt = datetime.datetime.fromisoformat(start_date)
            end_dt = datetime.datetime.fromisoformat(end_date)
            
            pipeline = [
                {"$match": {"payment_date": {"$gte": start_dt, "$lte": end_dt}}},
                {"$group": {"_id": None, "total_revenue": {"$sum": "$amount"}}}
            ]
            result = list(self._db.payments.aggregate(pipeline))
            total = result[0]["total_revenue"] if result else 0
            return f"Total revenue: {total}"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_client_stats(self):
        """Get client statistics (active/inactive counts)"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$status",
                        "count": {"$sum": 1}
                    }
                }
            ]
            result = list(self._db.clients.aggregate(pipeline))
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def get_attendance_stats(self, class_name: str = None):
        """Get attendance statistics for classes. Optionally filter by class name."""
        try:
            match_stage = {}
            if class_name:
                match_stage["name"] = {"$regex": class_name, "$options": "i"}
            
            pipeline = [
                {"$match": match_stage} if match_stage else {"$match": {}},
                {
                    "$project": {
                        "name": 1,
                        "instructor": 1,
                        "date": 1,
                        "attendee_count": {"$size": "$attendees"}
                    }
                }
            ]
            result = list(self._db.classes.aggregate(pipeline))
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def get_top_courses(self, limit: int = 5):
        """Get most popular courses by enrollment count"""
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "orders",
                        "localField": "_id",
                        "foreignField": "course_id",
                        "as": "enrollments"
                    }
                },
                {
                    "$project": {
                        "name": 1,
                        "instructor": 1,
                        "price": 1,
                        "enrollment_count": {"$size": "$enrollments"}
                    }
                },
                {"$sort": {"enrollment_count": -1}},
                {"$limit": limit}
            ]
            result = list(self._db.courses.aggregate(pipeline))
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def get_enrollment_trends(self):
        """Get enrollment trends by month"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": {
                            "year": {"$year": "$order_date"},
                            "month": {"$month": "$order_date"}
                        },
                        "enrollments": {"$sum": 1},
                        "revenue": {"$sum": "$amount"}
                    }
                },
                {"$sort": {"_id.year": 1, "_id.month": 1}}
            ]
            result = list(self._db.orders.aggregate(pipeline))
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def _run(self, input_str: str) -> str:
        """Main execution method for CrewAI tool"""
        try:
            # Parse the input JSON
            input_data = json.loads(input_str) if isinstance(input_str, str) else input_str
            
            action = input_data.get("action")
            if not action:
                return "Error: 'action' field is required."

            # Route to appropriate method based on action
            if action == "find_client":
                return json.dumps(self.find_client(input_data.get("query", {})), default=str)
            elif action == "get_client_orders":
                return json.dumps(self.get_client_orders(input_data.get("client_email")), default=str)
            elif action == "get_order_by_id":
                return json.dumps(self.get_order_by_id(input_data.get("order_id")), default=str)
            elif action == "get_payment_info":
                return json.dumps(self.get_payment_info(input_data.get("order_id")), default=str)
            elif action == "get_pending_payments":
                return json.dumps(self.get_pending_payments(), default=str)
            elif action == "get_classes_for_week":
                return json.dumps(self.get_classes_for_week(
                    input_data.get("start_date"), input_data.get("end_date")
                ), default=str)
            elif action == "get_courses_by_instructor":
                return json.dumps(self.get_courses_by_instructor(input_data.get("instructor")), default=str)
            elif action == "get_upcoming_classes":
                return json.dumps(self.get_upcoming_classes(), default=str)
            elif action == "calculate_revenue":
                return self.calculate_revenue(
                    input_data.get("start_date"), input_data.get("end_date")
                )
            elif action == "get_client_stats":
                return json.dumps(self.get_client_stats(), default=str)
            elif action == "get_attendance_stats":
                return json.dumps(self.get_attendance_stats(input_data.get("class_name")), default=str)
            elif action == "get_top_courses":
                return json.dumps(self.get_top_courses(input_data.get("limit", 5)), default=str)
            elif action == "get_enrollment_trends":
                return json.dumps(self.get_enrollment_trends(), default=str)
            else:
                return f"Unknown action: {action}"
                
        except json.JSONDecodeError as e:
            return f"Invalid JSON input: {str(e)}"
        except Exception as e:
            return f"Error executing MongoDB operation: {str(e)}"
