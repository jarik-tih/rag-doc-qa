from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.embeddings.openai import OpenAIEmbedding
#from app.core.config import OPEN_API_KEY

#OPENAI_EMBED_MODEL = OpenAIEmbedding(
#    model_name="text-embedding-3-small",
#    api_key= OPEN_API_KEY
#)

BGE_EMBED_MODEL = HuggingFaceEmbedding(
    model_name="BAAI/bge-base-en-v1.5"
)