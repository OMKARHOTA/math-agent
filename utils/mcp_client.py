# backend/utils/mcp_client.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")
TAVILY_ENDPOINT = "https://api.tavily.com/search"

def run_mcp(query, k=2):
    #we are using tavily api for external search
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "num_results": k
    }

    try:
        response = requests.post(TAVILY_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        results = response.json()

        # Extract and combine content snippets
        context = " ".join([r.get("content", "") for r in results.get("results", [])])
        return context.strip() or "No relevant web data found."
    except Exception as e:
        print(f" MCP search failed: {e}")
        return "Web search unavailable."


