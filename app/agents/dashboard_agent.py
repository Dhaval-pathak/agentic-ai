from crewai import Agent
from app.tools.mongodb_tool import MongoDBTool

import dotenv
import os

dotenv.load_dotenv()

# Initialize MongoDB tool for analytics
mongodb_tool = MongoDBTool(
    uri=os.getenv("MONGO_URI"),
    db_name=os.getenv("DB_NAME")
)

# Define Dashboard Agent
dashboard_agent = Agent(
    role="Dashboard Analytics Agent",
    goal="Provide comprehensive analytics and metrics for business insights including revenue, client stats, attendance, and enrollment trends.",
    tools=[mongodb_tool],
    backstory="""You are a specialized analytics agent that helps business owners understand their operations through data. 
    You excel at extracting insights from client data, revenue patterns, attendance records, and enrollment trends. 
    You present data in a clear, actionable format that helps in making business decisions.""",
    verbose=True,
    allow_delegation=False
)
