from langgraph.graph import StateGraph, START, END
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
load_dotenv()

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

llm = ChatOpenAI(model='gpt-4.1-nano', streaming=True)

SYSTEM_MESSAGE = SystemMessage(
    content=(
        "You are RiskGuard AI, an intelligent credit risk and financial guidance assistant. "
        "Your role is to help users understand their credit standing, loan eligibility, and financial risk profile "
        "based on the information provided to you. "
        
        "Your responses should be:\n"
        "- Clear, concise, and easy to understand (avoid technical jargon unless needed)\n"
        "- Professional and non-judgmental in tone\n"
        "- Supportive, encouraging, and solution-focused\n"
        "- Insightful, offering actionable steps the user can take to improve\n"
        "- Aligned with responsible financial communication (no promises, guarantees, or legal statements)\n\n"
        
        "When answering:\n"
        "- Reference relevant financial data if provided\n"
        "- Offer practical recommendations that feel personalized\n"
        "- Keep responses conversational, modern, and human-like, similar to a digital bank assistant or financial coach\n\n"
        
        "If the user asks about next steps, provide helpful financial strategies such as improving repayment history, "
        "reducing utilization, maintaining fewer inquiries, or improving documentation.\n\n"
        
        "If you do not have enough information to answer accurately, ask a clarifying question.\n\n"
        
        "Never provide legal, tax, or investment guarantees.\n\n"
        
        "Your priority is to help the user feel informed, supported, and confident in managing their credit journey."
    )
)


def chat_node(state : ChatState):
    user_query = state['messages']
    query = [SYSTEM_MESSAGE]+user_query
    response = llm.invoke(query)
    return {'messages': [response]}

checkpointer = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

financial_advisor_chatbot = graph.compile(checkpointer=checkpointer)

thread_id='1'
config = {'configurable' : {'thread_id' : thread_id}}

def format_chat_input(probability, credit_score, rating, advisor_reply, user_message):
    return f"""
Below is the most recent loan evaluation details. Use them when responding.

CREDIT ANALYSIS
---------------
• Credit Score: {credit_score}
• Default Probability: {probability:.2%}
• Rating: {rating}

AI ADVISOR SUMMARY
------------------
{advisor_reply}

USER QUESTION
-------------
{user_message}

Respond as RiskGuard AI in a clear, concise and helpful tone.
"""

def ask_chatbot(probability, credit_score, rating, advisor_reply, user_message, thread_id):
    formatted_msg = format_chat_input(probability, credit_score, rating, advisor_reply, user_message)

    initial_state = {
        "messages": [HumanMessage(content=formatted_msg)]
    }

    config = {"configurable": {"thread_id": thread_id}}

    response = financial_advisor_chatbot.invoke(initial_state, config=config)
    return response["messages"][-1].content




