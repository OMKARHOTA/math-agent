import axios from "axios";

const API_URL = "http://backend:8000";

// Send user query to backend
export const sendQuery = async (query) => {
  const res = await axios.post(`${API_URL}/api/query/ask`, { question: query });
  return res.data;
};

// Send feedback to backend
export const sendFeedback = async (query, answer, feedback,rating ) => {

    const res = await axios.post(`${API_URL}/api/feedback/submit`, {
    query,
    answer,
    feedback,rating
  });
  return res.data;
};
