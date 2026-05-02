def generate_response(company, product_area, decision):
    if decision == "escalated":
        return "Your request has been escalated to our support team for further assistance."

    if company.lower() == "hackerrank":
        return f"""Thanks for reaching out to HackerRank support.

It looks like you're facing an issue related to {product_area}.

We recommend:
- Checking platform requirements
- Verifying your setup and permissions
- Contacting recruiter/support if needed

If you need further assistance, please contact support.
"""

    elif company.lower() == "claude":
        return f"""Thanks for contacting Claude support.

It seems you're facing an issue related to {product_area}.

Please try:
- Checking API/configuration settings
- Verifying authentication
- Restarting your workflow

If the issue persists, please contact support.
"""

    elif company.lower() == "visa":
        return f"""Thank you for contacting Visa support.

We understand your concern regarding {product_area}.

Please note:
- Transactions depend on merchant policies
- Contact your bank for card-related issues
- For disputes, support will assist further

If you need further assistance, please contact support.
"""

    else:
        return "Thank you for reaching out. Please contact support for further assistance."