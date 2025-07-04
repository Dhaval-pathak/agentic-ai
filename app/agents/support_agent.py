from crewai import Agent
from app.tools.mongodb_tool import MongoDBTool
from app.tools.external_api_tool import ExternalAPITool
import dotenv
import os

dotenv.load_dotenv()

mongodb_tool = MongoDBTool(
    uri=os.getenv("MONGO_URI"),
    db_name=os.getenv("DB_NAME")
)

external_api_tool = ExternalAPITool(
    api_url=os.getenv("EXTERNAL_API_URL", "https://api.example.com"),
    api_key=os.getenv("EXTERNAL_API_KEY", "your_key")
)

# Define Support Agent
support_agent = Agent(
    role="Customer Support Agent",
    goal="""Handle all customer support queries including:
    - Client data searches and inquiries
    - Order management and status checks
    - Payment information and pending dues
    - Course and class discovery
    - Creating new client enquiries and orders
    """,
    tools=[mongodb_tool, external_api_tool],
    backstory="""You are a dedicated customer support agent with expertise in handling service-related queries.
    You have access to client databases and can create new orders and enquiries.
    You provide helpful, accurate information and can take action to resolve customer needs.
    Always be professional, helpful, and thorough in your responses.""",
    verbose=True,
    allow_delegation=False
)
