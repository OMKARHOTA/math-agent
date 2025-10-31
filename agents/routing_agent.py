from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def route_query(query):
    persist_dir = os.path.join("Backend", "data", "embeddings")

    # loading embedding model (must be same used in vector_db_agent)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # using FAISS vector database
    vectordb = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)

    # similar document searching
    results = vectordb.similarity_search_with_score(query, k=1)

    if results and results[0][1] < 0.4:
        print("Answer is on data.txt")
        return "KO"
    else:
        print("trying to search")
        return "WEB"
