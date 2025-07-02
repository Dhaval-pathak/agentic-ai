from crewai import Agent
from app.tools.mongodb_tool import MongoDBTool
from app.tools.external_api_tool import ExternalAPITool

# Initialize tools
mongodb_tool = MongoDBTool(uri="mongodb://localhost:27017", db_name="multi_agent")
external_api_tool = ExternalAPITool(api_url="https://api.example.com", api_key="your_key")

# Define Support Agent
support_agent = Agent(
    role="Support Agent",
    goal="Handle client, order, payment, and course queries; create orders/clients.",
    tools=[mongodb_tool, external_api_tool],
    backstory="You're a helpful support agent assisting users with service-related queries.",
)
