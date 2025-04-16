# src/agents/react_agent.py
import logging

from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

# We import the tool functions themselves
from src.tools.get_financials import get_financials
from src.tools.get_excel_data import get_excel_data
from src.tools.get_api_data import get_api_data

logger = logging.getLogger(__name__)


def build_agent(model_name="gpt-4o-mini", model_provider="openai"):
    """
    Build a ReAct agent with the given LLM model,
    hooking up any or all tools we want to expose.
    """
    llm = init_chat_model(model_name, model_provider=model_provider)

    # Tools array: each entry is a function (the "tool")
    # You can add or remove as your system grows
    tools = [get_financials, get_excel_data, get_api_data]

    # Create the ReAct agent
    agent_executor = create_react_agent(llm, tools)
    return agent_executor


def run_agent(agent_executor, user_query: str, stream=False):
    """
    Helper function to run the agent on a user query.
    Optionally stream the response.
    """
    messages = [HumanMessage(content=user_query)]

    if stream:
        # Stream the final message
        for step in agent_executor.stream({"messages": messages}, stream_mode="values"):
            step["messages"][-1].pretty_print()
    else:
        # Non-streaming approach
        # e.g. agent_executor.invoke(...) or agent_executor.run(...)
        # usage may differ slightly depending on your version
        result = agent_executor.invoke({"messages": messages})
        return result
