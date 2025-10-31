import React, { useState } from "react";
import { sendQuery } from "../api/agentApi";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await sendQuery(query);
      setResponse(res.answer || "No response received.");
    } catch (err) {
      setResponse("Error connecting to backend.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow-md">
      <h1 className="text-2xl font-bold mb-4 text-center">Math Routing Agent 🤖</h1>
      <textarea
        className="w-full p-3 border rounded-md"
        placeholder="Ask a math question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        onClick={handleSend}
        className="mt-3 w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>
      {response && (
        <div className="mt-4 p-4 bg-gray-100 rounded-md">
          <strong>Answer:</strong>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
