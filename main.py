from anthropic import Anthropic
import streamlit as st
from product_data import shoes_data
import json
import weave
import os
from dotenv import load_dotenv

load_dotenv()

weave.init("ecom-chat")

class AnthropicChatbot(weave.Model):
    system_prompt: str = ""
    model_name: str = "claude-2.0"
    max_tokens: int = 300

    def __init__(self):
        formatted_shoes_data = json.dumps(shoes_data, indent=2)
        self.system_prompt = f"""You are an e-commerce shopping assistant for a store that sells shoes. Answer questions about your store's products, and always provide a product link. The store name is ACME Shoes.

Available products:
{formatted_shoes_data}

Use this product information to answer customer queries accurately."""

    def predict(self, messages: list) -> str:
        client = Anthropic(api_key=st.session_state.anthropic_api_key)
        response = client.messages.create(
            model=self.model_name,
            system=self.system_prompt,
            messages=messages,
            max_tokens=self.max_tokens
        )
        return response.content[0].text

@weave.op()
def setup_sidebar():
    with st.sidebar:
        "[Get an Anthropic API key to put in your .env file](https://console.anthropic.com/settings/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/main.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

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

    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    if prompt := st.chat_input():
        if not anthropic_api_key:
            st.info("Please add your Anthropic API key to continue.")
            st.stop()

        st.session_state.anthropic_api_key = anthropic_api_key
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        model = AnthropicChatbot()
        response = model.predict(st.session_state.messages)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

anthropic_api_key = setup_sidebar()

run_chatbot()
