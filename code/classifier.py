def classify_request(issue):
    issue = issue.lower()

    # 🐞 Bug detection
    if any(word in issue for word in ["error", "not working", "fail", "issue", "bug"]):
        return "bug"

    # 💡 Feature request
    if any(word in issue for word in ["feature", "add", "improve", "request"]):
        return "feature_request"

    # ❌ Invalid / vague
    if len(issue.strip()) < 5 or issue in ["help", "it’s not working"]:
        return "invalid"

    # ✅ Default
    return "product_issue"


def classify_product_area(issue):
    issue = issue.lower()

    if any(word in issue for word in ["payment", "refund", "billing", "card"]):
        return "billing"

    if any(word in issue for word in ["login", "account", "access"]):
        return "account_access"

    if any(word in issue for word in ["test", "assessment", "interview"]):
        return "assessments"

    if any(word in issue for word in ["api", "model", "claude"]):
        return "api_support"

    return "general"


def infer_company(issue):
    issue = issue.lower()

    score = {
        "hackerrank": 0,
        "claude": 0,
        "visa": 0
    }

    # HackerRank keywords
    for word in ["test", "assessment", "interview", "candidate"]:
        if word in issue:
            score["hackerrank"] += 1

    # Claude keywords
    for word in ["api", "model", "claude", "bedrock"]:
        if word in issue:
            score["claude"] += 1

    # Visa keywords
    for word in ["card", "payment", "refund", "transaction"]:
        if word in issue:
            score["visa"] += 1

    return max(score, key=score.get)