# 🛍️ AWS production LLMs workshop
Our example is a simple e-commerce chatbot that lets you ask questions about products, and gives links as appropriate.

### Get an Anthropic API key

You can get your own Anthropic API key by following the following instructions:

1. Go to https://console.anthropic.com/.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

### Enter the Anthropic API key in your .env
1. Copy the .env.example file to .env
2. Enter the Anthropic API key into the .env file

```sh
ANTHROPIC_API_KEY='xxxxxxxxxx'
```

## Run it locally

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```
