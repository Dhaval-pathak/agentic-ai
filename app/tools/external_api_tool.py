import requests
from crewai.tools.base_tool import BaseTool
from pydantic import PrivateAttr
import json
from typing import Dict, Any

class ExternalAPITool(BaseTool):
    name: str = "ExternalAPITool"
    description: str = """Tool for creating clients and orders via external API.
    Available actions:
    - create_client: Create a new client enquiry
    - create_order: Create a new order for a client
    - create_enquiry: Create a general enquiry
    """
    _api_url: str = PrivateAttr()
    _headers: dict = PrivateAttr()

    def __init__(self, api_url, api_key, **data):
        super().__init__(**data)
        self._api_url = api_url
        self._headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    def create_client(self, client_data: Dict[str, Any]):
        """Create a new client"""
        try:
            # For demo purposes, simulate API call
            mock_response = {
                "success": True,
                "client_id": "client_123",
                "message": f"Client enquiry created for {client_data.get('name', 'Unknown')}",
                "data": client_data
            }
            return mock_response
            
            # Uncomment below for real API call
            # response = requests.post(f"{self._api_url}/clients", json=client_data, headers=self._headers)
            # return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_order(self, order_data: Dict[str, Any]):
        """Create a new order"""
        try:
            # For demo purposes, simulate API call
            mock_response = {
                "success": True,
                "order_id": "order_456",
                "message": f"Order created for {order_data.get('course_name', 'Unknown Course')}",
                "data": order_data,
                "status": "pending"
            }
            return mock_response
            
            # Uncomment below for real API call
            # response = requests.post(f"{self._api_url}/orders", json=order_data, headers=self._headers)
            # return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_enquiry(self, enquiry_data: Dict[str, Any]):
        """Create a general enquiry"""
        try:
            # For demo purposes, simulate API call
            mock_response = {
                "success": True,
                "enquiry_id": "enquiry_789",
                "message": "Enquiry submitted successfully",
                "data": enquiry_data
            }
            return mock_response
            
            # Uncomment below for real API call
            # response = requests.post(f"{self._api_url}/enquiries", json=enquiry_data, headers=self._headers)
            # return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run(self, input: str) -> str:
        """Main execution method for CrewAI tool"""
        try:
            # Parse the input - handle both string and dict formats
            if isinstance(input, str):
                actual_input = json.loads(input)
            else:
                actual_input = input.get("input", input)

            action = actual_input.get("action")
            if not action:
                return "Error: 'action' field is required."

            # Route to appropriate method
            if action == "create_client":
                result = self.create_client(actual_input.get("client_data", {}))
                return json.dumps(result)
            elif action == "create_order":
                result = self.create_order(actual_input.get("order_data", {}))
                return json.dumps(result)
            elif action == "create_enquiry":
                result = self.create_enquiry(actual_input.get("enquiry_data", {}))
                return json.dumps(result)
            else:
                return f"Unknown action: {action}"
                
        except Exception as e:
            return f"Error executing External API operation: {str(e)}"

    def _run(self, input: str) -> str:
        return self.run(input)
