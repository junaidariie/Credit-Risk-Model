from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# STATE
# =====================================================
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# =====================================================
# TOOL DEFINITIONS
# =====================================================

@tool
def tavily_search(query: str) -> dict:
    """
    Perform a web search using Tavily.
    Use this when up-to-date or factual information is required.
    """
    try:
        search = TavilySearchResults(max_results=5)
        results = search.run(query)
        return {"query": query, "results": results}
    except Exception as e:
        return {"error": str(e)}


tools = [tavily_search]


# =====================================================
# LLM CONFIGURATION
# =====================================================
llm = ChatOpenAI(
    model="gpt-4.1-nano",
    streaming=True
).bind_tools(tools)


# =====================================================
# SYSTEM PROMPT (MINIMALLY ENHANCED)
# =====================================================
SYSTEM_MESSAGE = SystemMessage(
    content=(
        "You are RiskGuard AI — an intelligent, production-grade credit risk and financial guidance assistant.\n\n"

        "You were designed and engineered by Junaid, an AI and Machine Learning practitioner with strong experience "
        "in data science, predictive modeling, and building real-world AI systems. "
        "This platform evolved from a simple classification model into a full-featured AI system with conversational intelligence, "
        "memory, real-time reasoning, and voice interaction.\n\n"

        "Your purpose is to help users understand their financial situation in a clear, calm, and human way — "
        "similar to how a knowledgeable financial advisor would explain things during a conversation.\n\n"

        "When responding, follow these principles:\n"
        "- Speak naturally and conversationally (avoid sounding like documentation)\n"
        "- Structure responses logically, but avoid numbered or rigid lists unless clearly helpful\n"
        "- Keep explanations clear, friendly, and easy to follow\n"
        "- Use short paragraphs instead of long blocks of text\n"
        "- Explain *why* something matters, not just *what* it is\n\n"

        "Your role includes:\n"
        "- Helping users understand their credit risk and financial standing\n"
        "- Explaining model-driven insights in plain language\n"
        "- Offering practical, realistic improvement suggestions\n"
        "- Supporting follow-up questions with context awareness\n\n"

        "You may reference system capabilities when useful, such as:\n"
        "- AI-based credit risk analysis\n"
        "- Context-aware conversations using memory\n"
        "- Real-time responses with streaming\n"
        "- Speech-to-text and text-to-speech interactions\n\n"

        "However, avoid technical deep dives unless the user explicitly asks for them.\n\n"

        "Tone guidelines:\n"
        "- Calm, professional, and reassuring\n"
        "- Confident but not authoritative\n"
        "- Helpful without being overwhelming\n\n"

        "Ethical guidelines:\n"
        "- Do not provide legal, tax, or investment guarantees\n"
        "- Avoid speculation or assumptions\n"
        "- Encourage informed and responsible decision-making\n\n"

        "Your ultimate goal is to help users feel informed, confident, and supported, "
        "while reflecting the quality and professionalism of a real-world financial AI system."
    )
)


# =====================================================
# CHAT NODE
# =====================================================
def chat_node(state: ChatState):
    messages = [SYSTEM_MESSAGE] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


# =====================================================
# GRAPH SETUP
# =====================================================
checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", ToolNode(tools))

# Routing logic
graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")
graph.add_edge("chat_node", END)

financial_advisor_chatbot = graph.compile(checkpointer=checkpointer)


# =====================================================
# INPUT FORMATTER
# =====================================================
def format_chat_input(probability, credit_score, rating, advisor_reply, user_message):
    return f"""
CREDIT ANALYSIS
---------------
Credit Score: {credit_score}
Default Probability: {probability:.2%}
Rating: {rating}

AI ADVISOR SUMMARY:
{advisor_reply}

USER MESSAGE:
{user_message}
"""


# =====================================================
# NORMAL RESPONSE (NON-STREAMING)
# =====================================================
def ask_chatbot(probability, credit_score, rating, advisor_reply, user_message, thread_id):

    formatted = format_chat_input(
        probability,
        credit_score,
        rating,
        advisor_reply,
        user_message
    )

    state = {"messages": [HumanMessage(content=formatted)]}
    config = {"configurable": {"thread_id": thread_id}}

    result = financial_advisor_chatbot.invoke(state, config=config)
    return result["messages"][-1].content


# =====================================================
# STREAMING RESPONSE
# =====================================================
def ask_chatbot_stream(probability, credit_score, rating, advisor_reply, user_message, thread_id):

    formatted = format_chat_input(
        probability,
        credit_score,
        rating,
        advisor_reply,
        user_message
    )

    state = {"messages": [HumanMessage(content=formatted)]}
    config = {"configurable": {"thread_id": thread_id}}

    for event in financial_advisor_chatbot.stream(state, config=config):
        if "messages" in event:
            msg = event["messages"][-1]
            if isinstance(msg, AIMessage) and msg.content:
                yield msg.content


