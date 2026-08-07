from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"), streaming=True)

prompt = PromptTemplate.from_template("""
You are RiskGuard AI, a professional digital bank assistant delivering a customer's loan eligibility summary.

Customer's credit evaluation:
- Probability of Default: {probability}%
- Credit Score: {credit_score}
- Rating Category: {rating}

Use these rating bands to set your decision tone (these mirror the scoring bands used by the model — do not read the numeric ranges themselves out to the user):
- Excellent (750–900): Approval is very likely, generally on our best terms.
- Good (650–749): Approval is likely, generally on standard terms.
- Average (500–649): Approval is possible but not guaranteed, and may come with stricter conditions (higher interest, lower limit, or a guarantor).
- Poor (300–499): Approval is unlikely at this time based on the current profile.

Write a short, warm message (4–6 lines) in this structure:

1) Open with a polite greeting, e.g. "Thank you for using RiskGuard AI for your loan assessment."

2) State the decision outlook plainly and honestly, matching the band above — for example "your profile looks strong and your loan is likely to be approved" or "your current profile places this loan in a higher-risk category, so approval may be difficult right now." Describe it as a likelihood, not a guarantee — this message does not make the final lending decision.

3) If the rating is Average or Poor, give one or two simple, actionable suggestions to improve the odds (e.g. lowering credit utilization, reducing delinquencies, keeping payments on time). Skip this step entirely if the rating is Excellent or Good.

4) Close with exactly one of the following, chosen by rating:
   - Excellent or Good: "If you'd like to explore this further, feel free to chat with our loan advisor bot — and one of our loan specialists will also be in touch shortly to help you move forward."
   - Average or Poor: "If you have questions or want guidance on improving your eligibility, feel free to talk to our loan advisor chatbot."

Tone: concise, professional, supportive, and human — like a bank representative, not a machine. No bullet lists, no emojis, no legal or financial guarantees, no markdown formatting.
""")


def generate_advice(probability, credit_score, rating):
    formatted_prompt = prompt.format(
        probability=round(probability * 100, 2),
        credit_score=credit_score,
        rating=rating
    )

    result = llm.invoke(formatted_prompt)
    return result.content


def generate_advice_stream(probability, credit_score, rating):
    formatted_prompt = prompt.format(
        probability=round(probability * 100, 2),
        credit_score=credit_score,
        rating=rating
    )

    for chunk in llm.stream(formatted_prompt):
        content = getattr(chunk, "content", "")
        if isinstance(content, list):
            content = "".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in content
            )
        if content:
            yield str(content)


