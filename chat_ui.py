import os
from dotenv import load_dotenv

import streamlit as st
from langchain_core.messages import HumanMessage

# Suppose we have a function that builds our agent
# from src.agents.react_agent import build_agent, run_agent
# We'll do a minimal version inline if you prefer.

###############################################################################
# 1) Load environment
###############################################################################
load_dotenv()

USERNAME = os.getenv("CHATAPP_USERNAME", "admin")
PASSWORD = os.getenv("CHATAPP_PASSWORD", "password123")


###############################################################################
# 2) Initialize a ReAct agent (example)
###############################################################################
# For demonstration, let's just mock out a "fake_agent" function
# In your real code, you might do something like:
#   agent = build_agent("gpt-4o-mini", model_provider="openai")
# Then define a function to call the agent with user messages.


def mock_agent_respond(user_query: str) -> str:
    # In reality, call your agent
    # result = run_agent(agent, user_query)  # or .invoke(...) depending on your setup
    return f"Agent response to: {user_query}"


###############################################################################
# 3) Streamlit UI with Basic Auth
###############################################################################
def check_credentials(username_input, password_input):
    """Return True if username/password match the environment vars."""
    return (username_input == USERNAME) and (password_input == PASSWORD)


def login_ui():
    """Renders sidebar login fields."""
    st.sidebar.title("Login")
    username_input = st.sidebar.text_input("Username", value="", key="login_username")
    password_input = st.sidebar.text_input(
        "Password", value="", type="password", key="login_password"
    )

    if st.sidebar.button("Login"):
        if check_credentials(username_input, password_input):
            st.session_state["logged_in"] = True
            # Store the logged-in username in session, separate from the widget key
            st.session_state["username"] = username_input
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password.")


def main():
    st.title("AnalystGPT Chat UI")

    # 3A) Check if user is logged in
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login_ui()
        return  # Stop rendering further if not logged in.

    # 3B) If logged in, show chat interface
    st.sidebar.success(f"Logged in as {st.session_state['username']}")

    # A place to store conversation history in session
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Chat input
    user_input = st.text_input("Ask a question:", value="")
    if st.button("Send") and user_input:
        # Add user query to conversation history
        st.session_state["messages"].append(("User", user_input))

        # Call the agent
        # In real code: response = run_agent(agent, user_input)
        response = mock_agent_respond(user_input)

        # Add agent response
        st.session_state["messages"].append(("Agent", response))

    # Display conversation
    for speaker, msg in st.session_state["messages"]:
        if speaker == "User":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Agent:** {msg}")

    # Optional logout button
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["messages"] = []
        st.rerun()


if __name__ == "__main__":
    main()
