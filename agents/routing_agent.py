from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from agents.math_solver import try_math_solver
import os
import re


def route_query(query: str):
    persist_dir = os.path.join("data", "embeddings")

    # ✅ Load embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)

    # ✅ Step 1: Search in FAISS
    results = vectordb.similarity_search_with_score(query, k=1)

    # ✅ If found in FAISS
    if results and results[0][1] < 0.4:
        print("📘 Answer is on data.txt")
        return "KO"

    else:
        # ✅ Step 2: Try math solver
        print("🧮 Not found in FAISS — trying math solver...")
        solver_result = try_math_solver(query)
        print(f"🧩 Solver result: {solver_result}")

        # ✅ Check if math solver succeeded
        if solver_result and not any(bad in solver_result.lower() for bad in [
            "sorry", "couldn't", "could not", "error", "invalid", "failed"
        ]):
            print("✅ Math solver succeeded!")
            return solver_result

        # ✅ If not solved by FAISS or math solver → LLM
        print("🌐 Not found anywhere — going for LLM")
        return "LLM"