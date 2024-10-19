import json
import weave
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from product_data import shoes_data

load_dotenv()

weave.init("ecom-chat")

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


class AnthropicChatbot(weave.Model):
    system_prompt: str = "You are a chatbot."
    model_name: str = "claude-2.0"
    max_tokens: int = 300

    def __init__(self, **data):
        super().__init__(**data)
        formatted_shoes_data = json.dumps(shoes_data, indent=2)
        self.system_prompt = f"""You are an e-commerce shopping assistant for a store that sells shoes. Answer questions about your store's products, and always provide a product link. The store name is ACME Shoes.

Available products:
{formatted_shoes_data}

Use this product information to answer customer queries accurately."""

    @weave.op()
    def predict(self, input: list | str) -> str:
        if isinstance(input, str):
            input = [
                {"role": "assistant", "content": "Hello! I'm your virtual shopping assistant. How can I help you?"},
                {"role": "user", "content": input}
            ]
        client = Anthropic()
        response = client.messages.create(
            model=self.model_name,
            system=self.system_prompt,
            messages=input,
            max_tokens=self.max_tokens
        )
        return response.content[0].text