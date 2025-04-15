import os
import openai

# Load environment
from dotenv import load_dotenv
load_dotenv()

# ---- Older (pinned) LangChain imports ----
from langchain.chat_models import init_chat_model
# from langchain.agents import Tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage


# Mock data
company_data = {
    "AAPL": {
        "overview": (
            "Apple Inc. is an American multinational technology company "
            "specializing in consumer electronics, software, and online services."
        ),
        "fundamentals": {
            "EPS": 6.05,
            "PE": 28.4,
            "revenue": 394.3,
            "revenue_unit": "USD (billions)"
        }
    }
}

def get_financials(input_ticker: str) -> str:
    """
    Get financial data for a given stock ticker.
    """
    ticker = input_ticker.strip(" '\"").upper()
    data = company_data.get(ticker)
    if not data:
        return f"No data found for ticker '{ticker}'."

    f = data["fundamentals"]
    overview = data["overview"]
    return (
        f"**Company:** {ticker}\n"
        f"**Overview:** {overview}\n\n"
        f"**EPS:** {f['EPS']}\n"
        f"**P/E Ratio:** {f['PE']}\n"
        f"**Revenue:** {f['revenue']} {f['revenue_unit']}\n"
    )

# financials_tool = Tool(
#     name="GetFinancialData",
#     func=get_financials,
#     description=(
#         "Use this tool to get fundamental financial data for a given stock ticker. "
#         "Input is the ticker symbol, e.g. 'AAPL'."
#     )
# )

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    if not openai.api_key:
        raise ValueError("No OPENAI_API_KEY found in environment. Check your .env file.")

    llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    agent_executor = create_react_agent(llm, [get_financials])

    
    # response = llm_with_tools.invoke(user_query)
    for step in agent_executor.stream(
        {"messages": [HumanMessage(content="What is Apple's current fundamentals?")]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()


if __name__ == "__main__":
    main()