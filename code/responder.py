def generate_response(results, ticket_text, company):
    if not results:
        return None, 0.0

    best = results[0]
    score = best["score"]

    text = ticket_text.lower()

    # ✅ Company intro
    if company == "HackerRank":
        intro = "Thanks for reaching out to HackerRank support.\n\n"
    elif company == "Claude":
        intro = "Thanks for contacting Claude support.\n\n"
    elif company == "Visa":
        intro = "Thank you for contacting Visa support.\n\n"
    else:
        intro = "Thank you for reaching out.\n\n"

    # 🔥 Smarter intent handling

    if "access" in text or "login" in text:
        body = """It seems you're having trouble accessing your account.

Please try the following:
- Verify your login credentials
- Reset your password if needed
- Contact your admin if your access was removed

If access was revoked, only the administrator can restore it."""

    elif "refund" in text or "payment" in text:
        body = """We understand your concern regarding payment or refund.

Please note:
- Refunds depend on platform policies
- Share your order ID with support for verification
- For card-related issues, your bank can assist further"""

    elif "not working" in text or "error" in text or "issue" in text:
        body = """It looks like you're facing a technical issue.

Try these steps:
- Refresh or restart your session
- Clear browser cache or try a different browser
- Check your internet connection

If the issue continues, please share details with support."""

    elif "interview" in text or "test" in text:
        body = """Regarding your test or interview:

- Ensure your system meets requirements
- Check browser, camera, and microphone permissions
- Contact the recruiter if rescheduling is needed"""

    elif "certificate" in text:
        body = """For certificate-related issues:

- Verify your profile details
- Try downloading the certificate again
- Contact support if corrections are required"""

    elif "security" in text or "fraud" in text:
        body = """This appears to be a sensitive security concern.

Please:
- Contact support immediately
- Avoid sharing sensitive details publicly
- Monitor your account activity"""

    else:
        body = """We understand your concern.

Please try basic troubleshooting steps or refer to the help section.
If the issue persists, contact support with more details."""

    response = f"""{intro}{body}

If you need further assistance, please contact support.
"""

    return response, score