import weave
from argparse import ArgumentParser
import os
from dotenv import load_dotenv
from chat_model import AnthropicChatbot
import streamlit as st
from product_data import shoes_data

load_dotenv()

weave.init("ecom-chat")

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

@weave.op()
def setup_sidebar():
    with st.sidebar:
        "[Get an Anthropic API key to put in your .env file](https://console.anthropic.com/settings/api-keys)"
    return None

@weave.op()
def run_chatbot():
    st.title("💬 Chatbot")
    st.caption("🚀 A Streamlit chatbot powered by Anthropic")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hello! I'm your virtual shopping assistant. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not anthropic_api_key:
            st.info("Please add your Anthropic API key to continue.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        model = AnthropicChatbot()
        response = model.predict(st.session_state.messages)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)


run_chatbot()