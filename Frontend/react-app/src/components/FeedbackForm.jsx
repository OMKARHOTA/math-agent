import React, { useState } from "react";
import { sendFeedback } from "../api/agentApi";

export default function FeedbackForm() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [rating, setRating] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!rating) {
      setStatus("Please select a rating (thumbs up or down)");
      return;
    }

    try {
      // ✅ FIXED: Pass parameters separately instead of as object
      const res = await sendFeedback(query, answer, feedback, rating);
      setStatus(res.message || "Feedback sent successfully!");
      setQuery("");
      setAnswer("");
      setFeedback("");
      setRating("");
    } catch (error) {
      console.error(error);
      setStatus("Error sending feedback.");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-6 rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">Feedback Form 📝</h2>

      <form onSubmit={handleSubmit}>
        <label className="block mb-2 text-gray-700 font-medium">Query</label>
        <input
          type="text"
          className="w-full p-3 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter the original question"
          required
        />

        <label className="block mb-2 text-gray-700 font-medium">Answer</label>
        <input
          type="text"
          className="w-full p-3 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Enter the answer received"
          required
        />

        <label className="block mb-2 text-gray-700 font-medium">Rating</label>
        <div className="flex gap-4 mb-4">
          <button
            type="button"
            className={`flex items-center justify-center gap-2 flex-1 p-3 border-2 rounded-md transition-all ${
              rating === "positive" 
                ? "border-green-500 bg-green-50 text-green-700" 
                : "border-gray-300 bg-gray-50 text-gray-700 hover:bg-gray-100"
            }`}
            onClick={() => setRating("positive")}
          >
            <span className="text-xl">👍</span>
            <span>Helpful</span>
          </button>

          <button
            type="button"
            className={`flex items-center justify-center gap-2 flex-1 p-3 border-2 rounded-md transition-all ${
              rating === "negative" 
                ? "border-red-500 bg-red-50 text-red-700" 
                : "border-gray-300 bg-gray-50 text-gray-700 hover:bg-gray-100"
            }`}
            onClick={() => setRating("negative")}
          >
            <span className="text-xl">👎</span>
            <span>Not Helpful</span>
          </button>
        </div>

        <label className="block mb-2 text-gray-700 font-medium">
          Feedback {rating === "negative" && "(Please suggest correct answer)"}
        </label>
        <textarea
          className="w-full p-3 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder={
            rating === "negative"
              ? "What was wrong? Please provide the correct answer..."
              : "Any additional comments..."
          }
          rows="4"
          required
        />

        <button
          type="submit"
          className="w-full bg-green-600 text-white py-3 rounded-md hover:bg-green-700 transition-colors font-medium"
        >
          Submit Feedback
        </button>
      </form>

      {status && (
        <p className={`mt-4 text-center text-sm font-medium ${
          status.includes("Error") || status.includes("Please") 
            ? "text-red-600" 
            : "text-green-600"
        }`}>
          {status}
        </p>
      )}

      <div className="mt-4 text-xs text-gray-500 text-center">
        <p>
          <strong>Helpful</strong>: Answer was correct and useful<br />
          <strong>Not Helpful</strong>: Answer was incorrect or unclear
        </p>
      </div>
    </div>
  );
}