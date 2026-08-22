from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.embeddings.openai import OpenAIEmbedding
#from app.core.config import OPEN_API_KEY

#OPENAI_EMBED_MODEL = OpenAIEmbedding(
#    model_name="text-embedding-3-small",
#    api_key= OPEN_API_KEY
#)
_bge_embed_model = None


def get_bge_embed_model():
    global _bge_embed_model

    if _bge_embed_model is None:
        _bge_embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-base-en-v1.5"
        )

    return _bge_embed_model