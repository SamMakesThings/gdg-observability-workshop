from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import streamlit as st

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="chatbot_api_key", type="password")
    "[Get an Anthropic API key](https://console.anthropic.com/settings/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Anthropic")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not anthropic_api_key:
        st.info("Please add your Anthropic API key to continue.")
        st.stop()

    client = Anthropic(api_key=anthropic_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    conversation = "\n\nHuman: " + "\n\nHuman: ".join([msg['content'] for msg in st.session_state.messages if msg['role'] == 'user'])
    conversation += "\n\nAssistant: " + "\n\nAssistant: ".join([msg['content'] for msg in st.session_state.messages if msg['role'] == 'assistant'])
    
    response = client.completions.create(
        model="claude-2",
        prompt=f"{conversation}\n\nHuman: {prompt}\n\nAssistant:",
        max_tokens_to_sample=300,
        stop_sequences=["\n\nHuman:"]
    )
    msg = response.completion.strip()
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
