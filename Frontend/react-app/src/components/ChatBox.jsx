import React, { useState, useRef } from "react";
import { sendQuery } from "../api/agentApi";
import FeedbackForm from "./FeedbackForm";

export default function ChatBox() {

  const [query, setQuery] = useState("");
  const [image, setImage] = useState(null);
  const [audio, setAudio] = useState(null);

  const [response, setResponse] = useState("");
  const [responseSource, setResponseSource] = useState("");

  const [lastQuery, setLastQuery] = useState("");

  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const fileInputRef = useRef(null);


  // -------- START RECORDING --------
  const startRecording = async () => {

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;

    mediaRecorder.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorder.onstop = () => {

      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });

      const audioFile = new File([audioBlob], "recording.webm");

      setAudio(audioFile);

      audioChunksRef.current = [];
    };

    mediaRecorder.start();
    setRecording(true);
  };


  // -------- STOP RECORDING --------
  const stopRecording = () => {

    mediaRecorderRef.current.stop();
    setRecording(false);

  };


  // -------- SEND QUERY --------
  const handleSend = async () => {

    if (!query && !image && !audio) return;

    setLoading(true);

    try {

      const res = await sendQuery(query, image, audio);

      setResponse(res.answer || "No response received.");
      setResponseSource(res.source || "");

      setLastQuery(query);

      // reset inputs
      setQuery("");
      setImage(null);
      setAudio(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

    } catch (err) {

      console.error(err);
      setResponse("Error connecting to backend.");

    }

    setLoading(false);
  };


  return (

    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow-md">

      <h1 className="text-2xl font-bold mb-4 text-center">
        Math Routing Agent 🤖
      </h1>


      {/* TEXT QUESTION */}

      <textarea
        className="w-full p-3 border rounded-md"
        placeholder="Ask a math question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />


      {/* IMAGE INPUT */}

      <input
        type="file"
        accept="image/*"
        className="mt-3"
        ref={fileInputRef}
        onChange={(e) => setImage(e.target.files[0])}
      />


      {/* AUDIO RECORDING */}

      <div className="mt-3 flex gap-2">

        {!recording ? (

          <button
            onClick={startRecording}
            className="bg-green-600 text-white px-4 py-2 rounded-md"
          >
            🎤 Start Recording
          </button>

        ) : (

          <button
            onClick={stopRecording}
            className="bg-red-600 text-white px-4 py-2 rounded-md"
          >
            ⏹ Stop Recording
          </button>

        )}

      </div>


      {/* ASK BUTTON */}

      <button
        onClick={handleSend}
        className="mt-4 w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>


      {/* RESPONSE */}

      {response && (

        <div className="mt-4 p-4 bg-gray-100 rounded-md">

          <strong>
            {responseSource === "HITL"
              ? "Clarification Needed:"
              : "Answer:"}
          </strong>

          <pre className="whitespace-pre-wrap mt-2 text-sm">
            {response}
          </pre>

        </div>

      )}


      {/* FEEDBACK FORM */}

      {response && responseSource !== "HITL" && (

        <FeedbackForm
          query={lastQuery}
          answer={response}
        />

      )}

    </div>

  );
}
