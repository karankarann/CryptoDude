```python
# app.py

import streamlit as st
from agent import agent_chain

# Set page title and intro
st.set_page_config(page_title="Trading Assistant Chatbot", layout="wide")
st.title("💬 Crypto/Forex Trading Assistant")
st.markdown("""
Ask any trading-related question about cryptocurrencies or forex, and the assistant will use real-time data to answer.
""")

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # You can optionally add a system or assistant welcome message:
    st.session_state.messages.append({"role": "assistant", "content": 
        "Hello! I'm your trading assistant bot. I can fetch live crypto/forex prices, calculate indicators like RSI, and provide news updates. "
        "Feel free to ask a question. *(Note: I am not a financial advisor. This is for educational purposes only.)*"
    })

# Display existing chat messages
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        with st.chat_message("user"):
            st.markdown(content)
    else:
        with st.chat_message("assistant"):
            st.markdown(content)

# Chat input box (Streamlit's new feature for chat apps)
if user_input := st.chat_input("Type your question here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display it immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    # Process the input with the agent (this may take a moment for the LLM and API calls)
    with st.spinner("Thinking..."):
        response = agent_chain.run(user_input)
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    # Display the assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
