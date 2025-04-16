# src/main.py
import os
from dotenv import load_dotenv

from src.agents.react_agent import build_agent, run_agent


def main():
    # 1) Load environment
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment. Check .env file.")

    # 2) Build the agent (ReAct) with desired tools
    agent_executor = build_agent(
        model_name="gpt-4o-mini",
        model_provider="openai",
    )

    # 3) Example user query
    user_query = "What is Apple's current fundamentals?"

    # 4) Run the agent (streaming or not)
    # In streaming mode:
    # run_agent(agent_executor, user_query, stream=True)

    # Non-streaming approach (returns a result dict usually):
    result = run_agent(agent_executor, user_query, stream=True)
    if result:
        print("=== Agent Final Response ===")
        # The exact shape of 'result' depends on how 'invoke' returns data
        # Typically, you'd do something like:
        final_message = result["messages"][-1]
        # or 'content' / 'text' depending on the structure
        print(
            final_message.content
            if hasattr(final_message, "content")
            else final_message
        )


if __name__ == "__main__":
    main()
