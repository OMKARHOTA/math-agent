from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from agents.routing_agent import route_query
from agents.vector_db import create_text
from agents.web_agent import run_math_agent
from utils.mcp_client import run_math_agent

router = APIRouter()

class QueryInput(BaseModel):
    question: str

class QueryResponse(BaseModel):
    source: str
    answer: str

@router.post("/ask", response_model=QueryResponse)
async def ask(query: QueryInput):
    try:
        user_question = query.question
        print(f"🧠 Received query: {user_question}")

        decision = route_query(user_question)
        print(f"📤 Routing result: {decision}")

        if decision == "KO":
            answer = create_text(user_question)
            return QueryResponse(source="Knowledge Base", answer=answer)

        elif decision == "WEB":
            answer = run_math_agent(user_question)
            return QueryResponse(source="LLM", answer=answer)

        else:
            # ✅ Math solver gave an actual answer
            return QueryResponse(source="Math Solver", answer=decision)

    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


