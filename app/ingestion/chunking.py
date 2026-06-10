from llama_index.core.node_parser import (
    TokenTextSplitter,
    SentenceSplitter,
    SemanticSplitterNodeParser
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def fixed_chunking(documents):
    splitter = TokenTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )
    return splitter.get_nodes_from_documents(documents)

def recursive_chunking(documents):
    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )
    return splitter.get_nodes_from_documents(documents)

embed_model=HuggingFaceEmbedding(
            model_name="BAAI/bge-base-en-v1.5"
)
def semantic_chunking(documents):
    splitter = SemanticSplitterNodeParser(
        embed_model=embed_model,
        buffer_size=1,
        breakpoint_percentile_threshold=95
    )
    return splitter.get_nodes_from_documents(documents)

