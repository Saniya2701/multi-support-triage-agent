def classify_ticket(ticket_text, company):
    text = ticket_text.lower()

    # Detect intent
    if "refund" in text or "payment" in text:
        request_type = "billing"
    elif "error" in text or "bug" in text or "not working" in text:
        request_type = "bug"
    elif "login" in text or "account" in text or "access" in text:
        request_type = "account"
    elif "fraud" in text or "stolen" in text:
        request_type = "fraud"
    else:
        request_type = "general"

    # Detect area
    if request_type == "billing":
        area = "billing"
    elif request_type == "bug":
        area = "technical_support"
    elif request_type == "account":
        area = "account_access"
    elif request_type == "fraud":
        area = "fraud_security"
    else:
        area = "general"

    return area, request_type