import requests
from crewai.tools.base_tool import BaseTool
from pydantic import PrivateAttr

class ExternalAPITool(BaseTool):
    name: str = "ExternalAPITool"
    description: str = "Tool for interacting with an external API for clients and orders."
    _api_url: str = PrivateAttr()
    _headers: dict = PrivateAttr()

    def __init__(self, api_url, api_key, **data):
        super().__init__(**data)
        self._api_url = api_url
        self._headers = {"Authorization": f"Bearer {api_key}"}
    
    def create_client(self, client_data):
        response = requests.post(f"{self._api_url}/clients", json=client_data, headers=self._headers)
        return response.json()
    
    def create_order(self, order_data):
        response = requests.post(f"{self._api_url}/orders", json=order_data, headers=self._headers)
        return response.json()

    def run(self, action, *args, **kwargs):
        # Example run method for CrewAI compatibility
        if action == "create_client":
            return self.create_client(*args, **kwargs)
        elif action == "create_order":
            return self.create_order(*args, **kwargs)
        else:
            return f"Unknown action: {action}"

    def _run(self, *args, **kwargs):
        return self.run(*args, **kwargs)