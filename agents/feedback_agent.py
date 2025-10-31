import sys
import os
import json
import dspy

# path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agents.routing_agent import route_query as math_agent

FEEDBACK = os.path.join("Backend", "data", "feedback_log.json")

#  DSPy
lm = dspy.LM("gpt-3.5-turbo")


class MathReasoner(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("question->answer")

    def forward(self, question):
        return self.prog(question=question)


# creating feedback file
def save_feedback(query: str, answer: str, feedback: str, rating: str = None):
    entry = {
        "query": query,
        "answer": answer,
        "feedback": feedback,
        "rating": rating  # ADDED RATING
    }

    if not os.path.exists(FEEDBACK):
        with open(FEEDBACK, "w") as f:
            json.dump([], f)

    with open(FEEDBACK, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=4)

    print(f"feedback is saved: {feedback.upper()}")


# optimizing the hyperparameters
def tuning(query, incorrect_answer, rating: str = None):
    example = [
        dspy.Example(question=query, answer="its incorrect").with_inputs("question"),
    ]

    # ✅ define the metric
    def simple_metric(example, pred, trace=None):
        try:
            gold_answer = example.answer.lower().strip()
            pred_answer = pred.answer.lower().strip()
            return 1.0 if gold_answer == pred_answer else 0.0
        except:
            return 0.0

    # wrapper class for math_agent
    class MathAgentWrapper(dspy.Module):
        def forward(self, question):
            result = math_agent(question)
            return dspy.Prediction(answer=result)

    # instance
    wrapper_model = MathAgentWrapper()

    # using BootstraoFewShot optimizer
    trainer = dspy.BootstrapFewShot(
        metric=simple_metric,
        max_bootstrapped_demos=1,
        max_labeled_demos=1
    )
    trainer.compile(wrapper_model, trainset=example)
    print("🧠 Model updated based on feedback.")


# ✅ Wrapper to get answer
def answer(query: str):
    result = math_agent(query)
    return result


# main test for dspy
def main():
    print("=== 🧠 Feedback Agent Test Run ===")
    query = "What is the integral of sin(x)?"

    # Step 1: Get model's answer
    ans = answer(query)
    print("Agent Answer:", ans)

    # Step 2: Simulate user feedback
    feedback = "Incorrect — the correct answer is -cos(x) + C"
    rating = "negative"  # ADDED RATING
    save_feedback(query, ans, feedback, rating)  # PASSED RATING

    # Step 3: Fine-tune the model
    tuning(query, incorrect_answer=ans, rating=rating)  # PASSED RATING


# for testing persopes
if __name__ == "__main__":
    main()
