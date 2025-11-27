from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

prompt = PromptTemplate.from_template("""
You are a financial credit risk advisor.  
Below is the user's credit evaluation:  

Probability of Default: {probability}%
Credit Score: {credit_score}
Credit Rating: {rating}

Write a professional but friendly response in 5-7 lines.  
Structure the message using:

1. Decision (approve or reject)
2. Simple explanation of why (based on numbers)
3. Suggested improvements to creditworthiness
4. Option for further help

Tone must feel like a modern digital bank assistant.
""")

def generate_advice(probability, credit_score, rating):
    formatted_prompt = prompt.format(
        probability=round(probability * 100, 2),
        credit_score=credit_score,
        rating=rating
    )

    result = llm.invoke(formatted_prompt)
    return result.content


#print(generate_advice(0.12, 750, 'good'))
