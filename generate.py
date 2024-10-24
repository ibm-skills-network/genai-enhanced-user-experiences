import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes

# watsonx.ai API client setup
my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    # "apikey": 'SKILLS-NETWORK' -- leave this commented out, we'll automatically inject credentials for you
}

client = APIClient(my_credentials)

# Define parameters for the watsonx.ai model
gen_parms = {
    GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
    GenParams.MAX_NEW_TOKENS: 2000  # Adjust the token limit as needed
}

model_id = 'meta-llama/llama-3-1-70b-instruct'
project_id = "skills-network"
space_id = None
verify = False

# Initialize the watsonx.ai ModelInference object
model = ModelInference(
    model_id=model_id,
    credentials=my_credentials,
    params=gen_parms,
    project_id=project_id,
    space_id=space_id,
    verify=verify
)

# Generic text generation function
def generate_text(prompt):
    """
    Generic function to generate text using watsonx.ai

    Args:
        prompt (str): The input prompt for the model to generate text.

    Returns:
        str: The generated text from watsonx.ai
    """
    try:
        # Generate text using watsonx.ai
        generated_response = model.generate_text(prompt=prompt, params=gen_parms)

        # Return the generated text
        return generated_response.strip()

    except Exception as e:
        print(f"Error generating text with watsonx.ai: {e}")
        return None
