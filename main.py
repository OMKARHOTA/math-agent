import os
os.environ["USE_TF"] = "0"
import sys

# Add the current directory to Python path so Backend imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.rag_router import router as rag_router
from router.feedback_router import router as feedback_router
app = FastAPI(
    title="Math Routing Agent ",
    description="Hello",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this later to your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Routers
app.include_router(rag_router, prefix="/api/query", tags=["RAG Router"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback Router"])
# Endpoint
@app.get("/")
async def root():
    return {"message": "Math Routing Agent API is on"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
