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
        "You are RiskGuard AI, a professional credit risk and loan advisory assistant. "
        "You help users understand their credit score, default probability, loan approval chances, "
        "and give practical, realistic suggestions to improve their profile. "
        "Be clear, polite, and avoid making guaranteed promises."
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

def seed_chat_memory(probability, credit_score, rating, advisor_reply, thread_id="default"):
    summary = (
        f"Here is the latest credit evaluation:\n"
        f"- Default Probability: {probability:.2%}\n"
        f"- Credit Score: {credit_score}\n"
        f"- Rating: {rating}\n\n"
        f"Advisor summary: {advisor_reply}\n"
        f"Use this information when responding to future questions."
    )

    config = {"configurable": {"thread_id": thread_id}}
    
    financial_advisor_chatbot.invoke(
        {"messages": [AIMessage(content=summary)]},
        config=config
    )