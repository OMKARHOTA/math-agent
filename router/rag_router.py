from fastapi import HTTPException, APIRouter, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import os
import uuid
import easyocr

from agents.routing_agent import route_query
from agents.vector_db import create_text
from agents.parser_agent import parse_problem
from agents.feedback_agent import ask_for_clarification

from utils.mcp_client import run_math_agent
from utils.audio_utils import transcribe_audio


router = APIRouter()

UPLOAD_DIR = os.path.join("data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load OCR model once
reader = easyocr.Reader(['en'])


class QueryResponse(BaseModel):
    source: str
    answer: str
    extracted_text: Optional[str] = None


@router.post("/ask", response_model=QueryResponse)
async def ask(
    question: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
):

    try:

        user_question = None

        print("Received:")
        print("Question:", question)
        print("Audio:", audio)
        print("Image:", image)

        # -------- IMAGE INPUT --------
        if image and image.filename:

            filename = f"{uuid.uuid4()}.png"
            image_path = os.path.join(UPLOAD_DIR, filename)

            with open(image_path, "wb") as f:
                f.write(await image.read())

            print("🖼 Image saved:", image_path)

            result = reader.readtext(image_path)

            user_question = " ".join([item[1] for item in result]).strip()

            print("OCR Extracted:", user_question)

        # -------- AUDIO INPUT --------
        elif audio and audio.filename:

            filename = f"{uuid.uuid4()}.webm"
            audio_path = os.path.join(UPLOAD_DIR, filename)

            with open(audio_path, "wb") as f:
                f.write(await audio.read())

            print("🎤 Audio saved:", audio_path)

            user_question = transcribe_audio(audio_path)

            print("Whisper Extracted:", user_question)

        # -------- TEXT INPUT --------
        elif question:

            user_question = question.strip()

        # -------- VALIDATION --------
        if not user_question:
            raise HTTPException(status_code=400, detail="No input provided")

        print("🧠 Raw Query:", user_question)

        # -------- PARSER AGENT --------
        parsed = parse_problem(user_question)

        print("Parsed Output:", parsed)

        # -------- HITL TRIGGER --------
        if parsed["needs_clarification"]:

            clarification = ask_for_clarification(parsed["problem_text"])

            return QueryResponse(
                source="HITL",
                answer=clarification,
                extracted_text=parsed["problem_text"]
            )

        # cleaned query
        cleaned_question = parsed["problem_text"]

        print("🧹 Cleaned Query:", cleaned_question)

        # -------- ROUTING AGENT --------
        decision = route_query(cleaned_question)

        # -------- KNOWLEDGE BASE --------
        if decision == "KO":

            answer = create_text(cleaned_question)

            return QueryResponse(
                source="Knowledge Base",
                answer=answer,
                extracted_text=cleaned_question
            )

        # -------- LLM --------
        elif decision == "LLM":

            answer = run_math_agent(cleaned_question)

            return QueryResponse(
                source="LLM",
                answer=answer,
                extracted_text=cleaned_question
            )

        # -------- MATH SOLVER --------
        else:

            return QueryResponse(
                source="Math Solver",
                answer=decision,
                extracted_text=cleaned_question
            )

    except Exception as e:

        print("ERROR:", e)

        raise HTTPException(status_code=500, detail=str(e))