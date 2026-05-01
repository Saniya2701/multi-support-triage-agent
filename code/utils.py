def fallback_response(ticket_text, company):

    if company == "HackerRank":
        return f"""Thanks for contacting HackerRank.

We understand your issue: "{ticket_text}"

Please try:
- Re-login to your account
- Check your browser compatibility
- Retry the test or action

If the issue persists, contact HackerRank support with details."""

    elif company == "Claude":
        return f"""Thanks for contacting Claude support.

We understand your concern: "{ticket_text}"

Try:
- Refreshing your session
- Checking API or service status
- Retrying the request

If the issue continues, please reach out to support."""

    elif company == "Visa":
        return f"""Thank you for contacting Visa.

Regarding: "{ticket_text}"

For security and billing concerns:
- Contact your issuing bank immediately
- Do not share sensitive details
- Monitor your transactions

For further help, please contact official Visa support."""

    else:
        return f"""Thank you for reaching out.

Regarding: "{ticket_text}"

Please try basic troubleshooting steps and contact support if needed."""