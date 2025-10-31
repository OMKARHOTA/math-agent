from agents.routing_agent import route_query
from utils.guardrails import validate_math_query, sanitize

def evaluate(txt_path:str):

    total,correct=0,0
    results=[]

    with open(txt_path,"r" ,encoding="utf-8") as f:
        content=f.read().strip().split("\n\n")

        for block in content:
            if not block.strip():
                continue

            lines = block.strip().split("\n")
            question=next((l[3:].strip() for l in lines if l.startswith("Q:")),None)
            expected=next((l[3:].strip().lower() for l in lines if l.startswith("A:")),"")

            if not question or not expected:
                continue

            if not validate_math_query(question):
                print(f"⚠️ Skipping invalid query: {question}")
                continue

            response=route_query(question)
            cleaned=sanitize(response).lower()

            is_right=expected in cleaned
            results.append({
                "Question": question,
                "Expected": expected,
                "ModelAnswer": cleaned,
                "Match": is_right
            })

            total+=1

            if is_right:
                correct+=1

    accuracy = (correct / total * 100) if total > 0 else 0.0


    print(f"{accuracy:.2f}% ({correct}/{total})")
    print(results)

if __name__ == "__main__":
    txt_file = "Backend/data/data.txt"
    evaluate(txt_file)