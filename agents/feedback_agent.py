import sys
import os
import json
import dspy
from datetime import datetime

# path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agents.routing_agent import route_query as math_agent

FEEDBACK = os.path.join("data", "feedback_log.json")

# DSPy setup
lm = dspy.LM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

dspy.settings.configure(lm=lm)


class MathReasoner(dspy.Module):

    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.prog(question=question)


# -------- DSPY HITL AGENT --------
class ClarificationAgent(dspy.Module):

    def __init__(self):
        super().__init__()
        self.generator = dspy.ChainOfThought("question -> clarification")

    def forward(self, question):
        return self.generator(question=question)


clarifier = ClarificationAgent()


def ask_for_clarification(question: str):

    result = clarifier(question=question)

    return result.clarification


# -------- SAVE FEEDBACK (MEMORY) --------
def save_feedback(
    query: str,
    answer: str,
    feedback: str,
    rating: str = None,
    parsed_question: dict = None,
    retrieved_context: str = None,
    verifier_outcome: str = None
):

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "original_input": query,
        "parsed_question": parsed_question,
        "retrieved_context": retrieved_context,
        "final_answer": answer,
        "verifier_outcome": verifier_outcome,
        "user_feedback": feedback,
        "rating": rating
    }

    if not os.path.exists(FEEDBACK):
        with open(FEEDBACK, "w") as f:
            json.dump([], f)

    with open(FEEDBACK, "r+") as f:

        data = json.load(f)
        data.append(entry)

        f.seek(0)
        json.dump(data, f, indent=4)

    print("🧠 Feedback stored in memory.")


# -------- MEMORY RETRIEVAL --------
def retrieve_similar(query: str):

    if not os.path.exists(FEEDBACK):
        return None

    with open(FEEDBACK, "r") as f:
        data = json.load(f)

    for item in data:

        if query.lower() in item["original_input"].lower():
            return item

    return None


# -------- MODEL TUNING --------
def tuning(query, incorrect_answer, rating: str = None):

    example = [
        dspy.Example(
            question=query,
            answer="its incorrect"
        ).with_inputs("question"),
    ]

    def simple_metric(example, pred, trace=None):

        try:
            gold_answer = example.answer.lower().strip()
            pred_answer = pred.answer.lower().strip()

            return 1.0 if gold_answer == pred_answer else 0.0

        except:
            return 0.0


    class MathAgentWrapper(dspy.Module):

        def forward(self, question):

            result = math_agent(question)

            return dspy.Prediction(answer=result)


    wrapper_model = MathAgentWrapper()

    trainer = dspy.BootstrapFewShot(
        metric=simple_metric,
        max_bootstrapped_demos=1,
        max_labeled_demos=1
    )

    trainer.compile(wrapper_model, trainset=example)

    print("🧠 Model updated based on feedback.")


# -------- ANSWER WITH MEMORY --------
def answer(query: str):

    memory = retrieve_similar(query)

    if memory:
        print("⚡ Using stored solution from memory.")
        return memory["final_answer"]

    result = math_agent(query)

    return result