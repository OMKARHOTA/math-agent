from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from agents.routing_agent import route_query
from agents.vector_db import create_text
from agents.web_agent import answer_from_web

router = APIRouter()

class QueryInput(BaseModel):
    question: str

class QueryResponse(BaseModel):
    source:str
    answer:str

@router.post("/ask",response_model=QueryResponse)
async def ask(query: QueryInput):
    try:
        user_question=query.question

        decision=route_query(user_question)
        print(f"Routing")

        if decision=="KO":
            answer=create_text(user_question)
            return QueryResponse(source='knowledge',answer=answer)
        elif decision=="WEB":
            answer=answer_from_web(user_question)
            return QueryResponse(source='Web search',answer=answer)

        else:
            return QueryResponse(source="System", answer="couldn't found")

    except Exception as e:
        print(f" Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

