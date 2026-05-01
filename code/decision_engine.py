from config import *

def decide(area, request_type, score):

    # Only strict for fraud
    if area in HIGH_RISK_AREAS:
        return "escalated", "high_risk_security"

    # Bugs → allow partial replies now
    if request_type == "bug" and score > 0.20:
        return "replied", "bug_guidance"

    # Medium risk → allow replies if decent score
    if area in MEDIUM_RISK_AREAS and score > 0.25:
        return "replied", "medium_risk_answered"

    if score >= REPLY_THRESHOLD:
        return "replied", "answer_from_corpus"

    if score >= ESCALATE_THRESHOLD:
        return "replied", "low_confidence_but_answered"

    return "escalated", "low_confidence"