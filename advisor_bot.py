from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

prompt = PromptTemplate.from_template("""
You are RiskGuard AI, a professional digital bank assistant.

Below is the user's credit evaluation:

• Probability of Default: {probability}%
• Credit Score: {credit_score}
• Rating Category: {rating}

Write a short, friendly message (4–6 lines) following this format:

1) A polite greeting such as:
   "Thank you for using RiskGuard AI for your loan assessment."

2) A clear decision tone:
   - If the score and risk level are strong: indicate the loan is likely suitable for approval.
   - If risk is high: indicate that approval may be difficult at this time.

3) Give one or two simple, actionable suggestions for improvement (if needed).

4) Close with a short support line such as:
   "If you have questions or want guidance, feel free to talk to our loan advisor chatbot."

Tone: concise, professional, supportive. No long bullet lists, no emojis, no legal claims.
""")


def generate_advice(probability, credit_score, rating):
    formatted_prompt = prompt.format(
        probability=round(probability * 100, 2),
        credit_score=credit_score,
        rating=rating
    )

    result = llm.invoke(formatted_prompt)
    return result.content


