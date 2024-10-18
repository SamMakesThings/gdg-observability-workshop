# 🛍️ AWS production LLMs workshop
Our example is a simple e-commerce chatbot that lets you ask questions about products, and gives links as appropriate.


### Get an Anthropic API key

You can get your own Anthropic API key by following the following instructions:

1. Go to https://console.anthropic.com/.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

### Enter the Anthropic API key in Streamlit Community Cloud

To set the Anthropic API key as an environment variable in Streamlit apps, do the following:

1. At the lower right corner, click on `< Manage app` then click on the vertical "..." followed by clicking on `Settings`.
2. This brings the **App settings**, next click on the `Secrets` tab and paste the API key into the text box as follows:

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
