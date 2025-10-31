import React from "react";
import ChatBox from "./components/ChatBox";
import FeedbackForm from "./components/FeedbackForm";
import bgImage from "./assets/math-bg.webp";

function App() {
  return (
    <div
      className="min-h-screen p-8 flex flex-col items-center gap-10"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed'
      }}
    >
      {/* Dark overlay for better text readability */}
      <div className="absolute inset-0 bg-black bg-opacity-40"></div>

      {/* Content container */}
      <div className="relative z-10 w-full flex flex-col items-center gap-10">
        <h1 className="text-4xl font-bold text-white mb-4 text-center drop-shadow-lg">
          Math Routing Agent 🧠
        </h1>

        {/* Chat Interface */}
        <div className="w-full max-w-2xl bg-white bg-opacity-95 rounded-xl shadow-2xl p-6">
          <ChatBox />
        </div>

        {/* Feedback Form */}
        <div className="w-full max-w-md bg-white bg-opacity-95 rounded-xl shadow-2xl p-6">
          <FeedbackForm />
        </div>
      </div>
    </div>
  );
}

export default App;