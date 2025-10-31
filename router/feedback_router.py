from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.feedback_agent import save_feedback, tuning

router = APIRouter()

class Feedback(BaseModel):
    query: str
    answer: str
    feedback: str
    rating:str=None# user’s correction or comment

@router.post("/submit")
async def submit_feedback(feedback: Feedback):
    try:
        save_feedback(feedback.query, feedback.answer, feedback.feedback)
        tuning(feedback.query, incorrect_answer=feedback.feedback)

        return {
            "status": "success",
            "message": "Feedback is saved and model updated successfully",
            "data": feedback.model_dump(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
