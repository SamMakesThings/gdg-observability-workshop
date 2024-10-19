from product_data import shoes_data
from evaluation_dataset import evaluation_data
from anthropic import Anthropic
import json
import asyncio
import re
import weave
from chat_model import AnthropicChatbot

# valid_links is of form List[str], or a list of strings.

# check to see if any link mentioned is present in a list of valid links
# valid_links = [
#	"https://store.com/about_us",
#	"https://store.com/product1",
#	"https://store.com/product2"
#]

shoe_links = [shoe["link"] for shoe in shoes_data]

@weave.op()
def are_links_valid(model_output: str):
	# Use a regular expression to check for links, then ensure it's an exact match for one of the links list

	url_pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'

	url_regex = re.compile(url_pattern, re.IGNORECASE)

	# Find all URLs in the text
	urls = url_regex.findall(model_output)
	
	# Check to see if found URLs are valid or not
	for url in urls:
		if url[0] not in shoe_links:  # Change: url[0] instead of url
			return False
	
	return True

@weave.op()
def is_response_length_good(model_output: str) -> bool:
    """
    Check if the model output is longer than 280 characters.
    
    Args:
    model_output (str): The string output from the model to be checked.
    
    Returns:
    bool: True if the output is longer than 280 characters, False otherwise.
    """
    return len(model_output) < 280

@weave.op()
async def is_accurate(reference_output: str, model_output: str) -> dict:
    evaluation_prompt = """You are an expert evaluator of chatbot responses. Your task is to compare an expected output with the actual model output and determine if they convey mostly the same information. Focus on the key points and overall meaning rather than exact wording.

    Expected Output: {reference_output}
    Model Output: {model_output}

    Evaluate if the Model Output conveys essentially the same information as the Expected Output. Provide your verdict as a JSON object with a single key "verdict" and a value of 1 if they match closely, or 0 if they differ significantly.

    Output in only valid JSON format.
    """

    client = Anthropic()

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=300,
        messages=[
            {"role": "user", "content": evaluation_prompt.format(
                reference_output=reference_output,
                model_output=model_output
            )}
        ],
        # response_format={"type": "json_object"}
    )

    result = json.loads(response.content[0].text)
    return {
        "verdict": result["verdict"] == 1
    }





model = AnthropicChatbot()

evaluation = weave.Evaluation(  
    name='general_evals',  
    dataset=evaluation_data,
    scorers=[are_links_valid, is_response_length_good, is_accurate]
)

print(asyncio.run(evaluation.evaluate(model)))



