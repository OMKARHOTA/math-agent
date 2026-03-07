from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.feedback_agent import save_feedback, tuning

router = APIRouter()


class Feedback(BaseModel):
    query: str
    answer: str
    feedback: str
    rating: str | None = None
    parsed_question: dict | None = None
    retrieved_context: str | None = None
    verifier_outcome: str | None = None


@router.post("/submit")
async def submit_feedback(feedback: Feedback):

    try:

        save_feedback(
            query=feedback.query,
            answer=feedback.answer,
            feedback=feedback.feedback,
            rating=feedback.rating,
            parsed_question=feedback.parsed_question,
            retrieved_context=feedback.retrieved_context,
            verifier_outcome=feedback.verifier_outcome
        )

        tuning(
            feedback.query,
            incorrect_answer=feedback.answer,
            rating=feedback.rating
        )

        return {
            "status": "success",
            "message": "Feedback saved and model updated",
            "data": feedback.model_dump()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
