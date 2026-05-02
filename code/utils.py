def assess_risk(issue):
    issue = issue.lower()

    # 🚨 ONLY VERY STRICT high-risk keywords
    high_risk_keywords = [
        "fraud", "stolen card", "unauthorized transaction",
        "identity theft"
    ]

    for word in high_risk_keywords:
        if word in issue:
            return "high"

    return "low"