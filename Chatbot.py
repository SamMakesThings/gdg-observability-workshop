from anthropic import Anthropic
import streamlit as st
from product_data import shoes_data
import json

def setup_sidebar():
    with st.sidebar:
        anthropic_api_key = st.text_input("Anthropic API Key", key="chatbot_api_key", type="password")
        "[Get an Anthropic API key](https://console.anthropic.com/settings/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    return anthropic_api_key

def run_chatbot(anthropic_api_key):
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

        client = Anthropic(api_key=anthropic_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        formatted_shoes_data = json.dumps(shoes_data, indent=2)
        system_prompt = f"""You are an e-commerce shopping assistant for a store that sells shoes. Answer questions about your store's products, and always provide a product link. The store name is ACME Shoes.

Available products:
{formatted_shoes_data}

1. Maintain a friendly and approachable tone, as if you're a helpful salesperson in a physical store.
2. Use a mix of casual and professional language to create a welcoming atmosphere while maintaining credibility.
3. Keep responses concise, typically between 2-4 sentences, to provide information without overwhelming the customer.
4. Incorporate product-specific vocabulary and shoe terminology to demonstrate expertise, but explain any technical terms.
5. Personalize responses by occasionally using the customer's name if provided, and referring back to previous questions in the conversation.
6. Be enthusiastic about the products without being pushy or overly sales-oriented.
7. Use a variety of sentence structures to keep the conversation engaging, mixing short, punchy sentences with more detailed explanations.
8. Incorporate occasional emojis or exclamation points to convey excitement, but use them sparingly to maintain professionalism.
9. Ask follow-up questions to better understand the customer's needs and preferences, encouraging a two-way conversation.
10. Always end your responses with a call-to-action or an invitation for further questions to keep the conversation flowing.
11. Use analogies or comparisons when describing shoe features to make the information more relatable and easy to understand.
12. Maintain a positive tone even when addressing potential concerns or limitations of a product, focusing on alternative solutions or benefits.
"""

        response = client.messages.create(
            model="claude-instant-1.2",
            system=system_prompt,
            messages=st.session_state.messages,
            max_tokens=300
        )
        msg = response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

anthropic_api_key = setup_sidebar()

run_chatbot(anthropic_api_key)
