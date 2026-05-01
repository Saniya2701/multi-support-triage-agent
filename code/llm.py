import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_llm_response(ticket_text, company):

    prompt = f"""
You are a professional customer support agent.

Company: {company}

User Issue:
{ticket_text}

Instructions:
- Give a clear, helpful, and polite response
- Do NOT promise refunds or actions you cannot guarantee
- Provide steps if possible
- Keep it concise and human-like

Response:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"