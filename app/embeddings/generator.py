from app.embeddings.models import (
BGE_EMBED_MODEL,
#OPENAI_EMBED_MODEL
)

def generate_bge_embeddings(texts):
    return BGE_EMBED_MODEL.get_text_embedding_batch(texts)

#def generate_openai_embeddings(texts):
    return OPENAI_EMBED_MODEL.get_text_embedding_batch(texts)
