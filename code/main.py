import csv
import pandas as pd
from retriever import Retriever
from classifier import classify_ticket
from responder import generate_response
from decision_engine import decide
from utils import fallback_response
from config import *

print("="*70)
print("🔥 Advanced Multi-Support Triage Agent")
print("="*70)

# ✅ Load dataset
df = pd.read_csv("../support_tickets/support_tickets.csv")

documents = df["Issue"].dropna().tolist()
retriever = Retriever(documents)

print(f"\n📚 Indexed {len(documents)} documents")
print(f"✅ Loaded {len(df)} tickets")

output = []

print("\n🔄 Processing tickets...")

for i, row in df.iterrows():

    text = str(row["Issue"])
    company = str(row["Company"])

    if (i+1) % 5 == 0:
        print(f"   [{i+1}/{len(df)}]")

    # ✅ Classification
    area, request_type = classify_ticket(text, company)

    # ✅ Retrieval
    results = retriever.search(text)

    # ✅ Base response
    response, score = generate_response(results, text, company)

    # ✅ Decision
    decision, justification = decide(area, request_type, score)

    # 🔥 FINAL LOGIC (NO OPENAI)
    if decision == "replied":
        # Use fallback if low confidence
        if score < 0.30:
            response = fallback_response(text, company)

    if decision == "escalated":
        response = "Please contact support for further assistance."

    # ✅ ALWAYS append
    output.append({
        "status": decision,
        "product_area": area,
        "response": response,
        "justification": justification,
        "request_type": request_type
    })

# ✅ Safe CSV writing
if output:
    with open("../support_tickets/output.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)

    print("\n" + "="*70)
    print("✅ DONE!")
    print(f"🔥 Replied: {sum(1 for o in output if o['status']=='replied')}")
    print(f"⚠️ Escalated: {sum(1 for o in output if o['status']=='escalated')}")
    print("📁 Output: ../support_tickets/output.csv")
    print("="*70)
else:
    print("⚠️ No output generated!")