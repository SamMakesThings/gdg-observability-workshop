# 🛒 GDG production LLMs workshop
Our example is a simple e-commerce chatbot that lets you ask questions about products, and gives links as appropriate.

### Get a Groq API key
You can get your own Groq API key by following the following instructions:

1. Go to https://console.groq.com/.
2. Click on the `API Keys` button on the left sidebar, then on "Create API Key".
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

### Enter the Groq API key in your .env
1. Copy the .env.example file to .env
2. Enter the Groq API key into the .env file

```sh
GROQ_API_KEY='xxxxxxxxxx'
```

## Run the app locally

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```


## Running evals (requires completing the exercises)

```sh
python evals.py
```
OR, to run the demo evals, use `python evals_completed.py`