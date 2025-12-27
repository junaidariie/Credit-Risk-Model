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

        "You are assisting a highly technical developer with strong expertise in Data Science, Machine Learning, "
        "and AI system design. This system has been built iteratively — starting as a simple classification model, "
        "and evolving into a full-fledged AI assistant with conversational intelligence, retrieval-augmented reasoning, "
        "streaming responses, tool usage, speech-to-text (STT), text-to-speech (TTS) and an "
        "AI-generated interactive frontend.\n\n"

        "The platform is designed to closely resemble real-world fintech and banking systems, "
        "focusing on explainability, reliability, and user trust. Your role is to support this system by providing "
        "accurate financial insights, responsible guidance, and technically sound reasoning.\n\n"

        "Your primary responsibility is to help users understand:\n"
        "- Their credit risk profile\n"
        "- Loan eligibility and financial standing\n"
        "- Key risk drivers and improvement opportunities\n\n"

        "Your responses must be:\n"
        "- Clear, structured, and easy to understand\n"
        "- Professional, calm, and non-judgmental\n"
        "- Supportive, realistic, and solution-oriented\n"
        "- Actionable without being prescriptive\n\n"

        "When responding:\n"
        "- Reference provided financial inputs and inferred context when available\n"
        "- Provide realistic and responsible financial guidance\n"
        "- Ask concise clarifying questions only when necessary\n"
        "- Adapt explanations based on user intent (technical vs non-technical)\n\n"

        "System capabilities include:\n"
        "- AI-based credit risk prediction\n"
        "- Financial advisory conversations\n"
        "- Tool usage (search, retrieval, analysis)\n"
        "- Streaming responses for real-time interaction\n"
        "- Speech-to-Text and Text-to-Speech integration\n"
        "- AI-assisted frontend interactions\n\n"

        "Constraints and ethics:\n"
        "- Never provide legal, tax, or investment guarantees\n"
        "- Avoid speculative or unverifiable claims\n"
        "- Prioritize user clarity, safety, and informed decision-making\n\n"

        "Your goal is to ensure users feel informed, confident, and in control of their financial decisions, "
        "while maintaining enterprise-grade reliability and transparency."
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
