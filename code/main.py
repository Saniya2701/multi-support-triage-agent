import pandas as pd
from classifier import classify_request, classify_product_area, infer_company
from retriever import retrieve_documents
from utils import assess_risk
from decision_engine import decide_action   # ✅ IMPORTANT

print("="*70)
print("🔥 Advanced Multi-Support Triage Agent")
print("="*70)

# 📂 Load CSV
df = pd.read_csv("../support_tickets/support_tickets.csv")

print(f"\n📚 Loaded {len(df)} tickets\n")

output = []
replied = 0
escalated = 0

print("🔄 Processing tickets...")

for i, row in df.iterrows():
    issue = str(row.get("Issue", "")).strip()
    subject = str(row.get("Subject", "")).strip()
    company = str(row.get("Company", "")).strip().lower()

    full_text = subject + " " + issue

    # 🏢 Company inference
    if company == "" or company == "nan":
        company = infer_company(full_text)

    # 🧠 Classification
    request_type = classify_request(full_text)
    product_area = classify_product_area(full_text)

    # 📚 Retrieval
    doc, score = retrieve_documents(full_text, company)

    # ⚠️ Risk
    risk = assess_risk(full_text)

    # ✅ CENTRALIZED DECISION ENGINE (THIS FIXES EVERYTHING)
    decision, reason = decide_action(
        request_type,
        product_area,
        risk,
        score
    )

    # 📊 Count
    if decision == "replied":
        replied += 1
    else:
        escalated += 1

    # 📝 Response
    if decision == "replied":
        if doc:
            response = f"Based on our documentation:\n\n{doc[:300]}..."
        else:
            response = "Thank you for reaching out. Please try basic troubleshooting steps or contact support if the issue persists."
    else:
        response = "Your request requires further review. Our support team will assist you shortly."

    # 📦 Save output
    output.append({
        "status": decision,
        "product_area": product_area,
        "response": response,
        "justification": reason,
        "request_type": request_type
    })

    # 🖥️ Print logs
    print(f"TICKET_{i+1} | {company} | {request_type} | {decision} | {round(score,3)} | {reason}")

# 💾 Save CSV
out_df = pd.DataFrame(output)
out_df.to_csv("../support_tickets/output.csv", index=False)

print("\n" + "="*70)
print("✅ DONE!")
print(f"🔥 Replied: {replied}")
print(f"⚠️ Escalated: {escalated}")

total = replied + escalated
if total > 0:
    print("\n📊 PERFORMANCE METRICS")
    print(f"Automation Rate: {(replied/total)*100:.2f}%")
    print(f"Escalation Rate: {(escalated/total)*100:.2f}%")

print("="*70)