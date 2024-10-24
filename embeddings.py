from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes


def get_embeddings(text: str): 


    my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    # "apikey": 'SKILLS-NETWORK' -- leave this commented out, we'll automatically inject credentials for you
    }

    model_id = EmbeddingTypes.IBM_SLATE_30M_ENG
    project_id = "skills-network"
    space_id = None
    verify = False

# Set the truncate_input_tokens to a value that is equal to or less than the maximum allowed tokens for the embedding model that you are using. If you don't specify this value and the input has more tokens than the model can process, an error is generated.

    embed_params = {
    EmbedParams.TRUNCATE_INPUT_TOKENS: 128,
    EmbedParams.RETURN_OPTIONS: {
        'input_text': True
    }
    }


    embedding = Embeddings(
    model_id=model_id,
    credentials=my_credentials,
    params=embed_params,
    project_id=project_id,
    space_id=space_id,
    verify=verify
    )

    embedding_vectors = embedding.embed_documents(texts=[text])[0]

    return embedding_vectors
