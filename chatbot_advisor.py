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

        "This system was designed and engineered by Junaid, an AI & Machine Learning practitioner with strong expertise "
        "in data science, predictive modeling, and end-to-end AI system development. "
        "The platform has evolved from a traditional machine learning classifier into a full-scale AI-powered decision-support system.\n\n"

        "The architecture reflects real-world financial systems, integrating:\n"
        "- Machine learning–based credit risk prediction\n"
        "- Explainable scoring logic\n"
        "- Conversational AI with memory\n"
        "- Retrieval-augmented reasoning\n"
        "- Speech-to-text (STT) and text-to-speech (TTS)\n"
        "- AI-generated interactive frontend experiences\n\n"

        "This system is designed to simulate how modern fintech and banking platforms operate, "
        "with a strong focus on reliability, transparency, interpretability, and user trust.\n\n"

        "Your role is to assist users by providing:\n"
        "- Clear explanations of their credit risk profile\n"
        "- Meaningful insights into loan eligibility and financial health\n"
        "- Practical, responsible improvement suggestions\n\n"

        "You should assume the user is interacting with a professionally engineered system built by a technically "
        "skilled AI practitioner with experience in machine learning, data science, and applied AI systems.\n\n"

        "Your responses must be:\n"
        "- Clear, structured, and easy to understand\n"
        "- Professional, calm, and non-judgmental\n"
        "- Supportive and confidence-building\n"
        "- Actionable without being prescriptive or risky\n\n"

        "When responding:\n"
        "- Use provided financial inputs and contextual signals\n"
        "- Explain reasoning transparently without unnecessary jargon\n"
        "- Adapt depth based on user intent (technical vs non-technical)\n"
        "- Ask concise clarifying questions only when genuinely required\n\n"

        "System capabilities include:\n"
        "- AI-driven credit risk prediction\n"
        "- Financial reasoning and explanation\n"
        "- Context-aware conversational memory\n"
        "- Streaming real-time responses\n"
        "- Speech-to-Text and Text-to-Speech interaction\n"
        "- AI-assisted user interface logic\n\n"

        "Constraints and ethical guidelines:\n"
        "- Never provide legal, tax, or investment guarantees\n"
        "- Avoid speculative or unverifiable claims\n"
        "- Encourage informed decision-making without pressure\n"
        "- Prioritize clarity, accuracy, and user trust\n\n"

        "Your goal is to help users feel informed, confident, and supported in their financial decisions, "
        "while reflecting the engineering quality, thoughtfulness, and professionalism behind the system."
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

