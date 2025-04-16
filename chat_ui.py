import os
from dotenv import load_dotenv
import streamlit as st

from src.agents.react_agent import build_agent

load_dotenv()

USERNAME = os.getenv("CHATAPP_USERNAME", "admin")
PASSWORD = os.getenv("CHATAPP_PASSWORD", "password123")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def check_credentials(username_input, password_input):
    return (username_input == USERNAME) and (password_input == PASSWORD)


def login_ui():
    st.sidebar.title("Login")
    username_input = st.sidebar.text_input("Username", value="", key="login_username")
    password_input = st.sidebar.text_input(
        "Password", value="", type="password", key="login_password"
    )

    if st.sidebar.button("Login"):
        if check_credentials(username_input, password_input):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            st.session_state["messages"] = []
            st.session_state["agent"] = None
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password.")


def main():
    st.set_page_config(
        page_title="Chatbot Demo (Streaming)", page_icon="💬", layout="centered"
    )
    st.title("💬 Streaming Chatbot")
    st.caption("A Streamlit chatbot that streams tokens as they arrive.")

    if not OPENAI_API_KEY:
        st.error("No OpenAI API key found in environment. Please set OPENAI_API_KEY.")
        st.stop()

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login_ui()
        return

    with st.sidebar:
        st.write("You are logged in as:", st.session_state["username"])
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["messages"] = []
            st.session_state["agent"] = None
            st.rerun()

    # Build the agent once
    if "agent" not in st.session_state or st.session_state["agent"] is None:
        agent_executor = build_agent(model_name="gpt-4o-mini", model_provider="openai")
        st.session_state["agent"] = agent_executor

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hello! How can I help you today?"}
        ]

    # Display existing conversation
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Type your message here...")
    if user_input:
        # 1) Display user message immediately
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # 2) Now let's stream the agent's response token by token
        response_text = ""
        assistant_placeholder = st.chat_message(
            "assistant"
        )  # create "assistant" bubble
        agent = st.session_state["agent"]

        # We'll pass something like {"messages": [HumanMessage(content=user_input)]}
        # and ask for stream_mode="values"
        from langchain_core.messages import HumanMessage

        messages = [HumanMessage(content=user_input)]

        for step in agent.stream({"messages": messages}, stream_mode="values"):
            # Each 'step' typically has the partial or updated content in step["messages"][-1].content
            partial_text = step["messages"][-1].content
            # If partial_text is the entire text so far, just overwrite.
            # Or we can accumulate if it returns only the chunk diff.
            response_text = partial_text
            assistant_placeholder.write(response_text)

        # 3) Once done, store final assistant message in session
        st.session_state["messages"].append(
            {"role": "assistant", "content": response_text}
        )


if __name__ == "__main__":
    main()
