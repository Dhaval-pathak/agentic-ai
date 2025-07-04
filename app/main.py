from fastapi import FastAPI, HTTPException
from crewai import Task, Crew
from pydantic import BaseModel
from app.agents.support_agent import support_agent
from app.agents.dashboard_agent import dashboard_agent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    agent_type: str  # "support" or "dashboard"
@app.get("/")
def home():
    return ("Hello backend is live")
@app.post("/query")
async def process_query(request: QueryRequest):
    try:
        logger.info(f"Processing {request.agent_type} query: {request.query}")
        
        if request.agent_type == "support":
            task = Task(
                description=f"""Handle this customer support query: {request.query}
                
                Use the available tools to:
                1. Search for relevant client, order, payment, or course information
                2. Create new orders or enquiries if requested
                3. Provide comprehensive and helpful responses
                
                Available tools: MongoDBTool (for data queries), ExternalAPITool (for creating orders/clients)""",
                agent=support_agent,
                expected_output="A detailed and helpful response to the customer support query with specific data and actionable information."
            )
            crew = Crew(
                agents=[support_agent],
                tasks=[task],
                verbose=True
            )
            result = crew.kickoff()
            return {"agent_type": "support", "response": str(result)}
            
        elif request.agent_type == "dashboard":
            task = Task(
                description=f"""Provide analytics and metrics for this business query: {request.query}
                
                Use the MongoDB tool to:
                1. Calculate revenue metrics and financial insights
                2. Analyze client statistics and behavior
                3. Provide enrollment and attendance analytics
                4. Generate business intelligence reports
                
                Available tools: MongoDBTool (for analytics queries)""",
                agent=dashboard_agent,
                expected_output="A comprehensive analytics report with specific metrics, trends, and business insights."
            )
            crew = Crew(
                agents=[dashboard_agent],
                tasks=[task],
                verbose=True
            )
            result = crew.kickoff()
            return {"agent_type": "dashboard", "response": str(result)}
            
        else:
            raise HTTPException(status_code=400, detail="Invalid agent type. Use 'support' or 'dashboard'")
            
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")