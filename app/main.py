from fastapi import FastAPI
from crewai import Task, Crew
from pydantic import BaseModel
from app.agents.support_agent import support_agent

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    agent_type: str  # "support" or "analytics"

@app.post("/query")
async def process_query(request: QueryRequest):
    if request.agent_type == "support":
        task = Task(
            description=request.query,
            agent=support_agent,
            expected_output="A helpful answer to the user's support query."
        )
        crew = Crew(
            agents=[support_agent],
            tasks=[task]
        )
        result = crew.kickoff()
        return {"response": result}
    elif request.agent_type == "analytics":
        return {"error": "Analytics agent is not implemented yet."}
    else:
        return {"error": "Invalid agent type"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Agent System API. Use /query to interact with agents."}