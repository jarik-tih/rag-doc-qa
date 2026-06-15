import time

from app.embeddings.generator import (
generate_bge_embeddings,
#generate_openai_embeddings
)
from app.embeddings.utils import (
load_chunks,
save_embeddings
)

chunks = load_chunks("../data/processed/recursive_nodes.json")
texts = [chunk["text"] for chunk in chunks]

# BGE
start = time.perf_counter()

bge_embeddings = generate_bge_embeddings(texts)
bge_time = time.perf_counter() - start
print("BGE: ", bge_time)

save_embeddings(bge_embeddings, "../data/processed/bge_embeddings.json")
# OpenAI

#start = time.perf_counter()
#openai_embeddings = generate_openai_embeddings(texts)
#openai_time = time.perf_counter() - start
#print("OpenAI: ", openai_time)
#save_embeddings(openai_embeddings, "../data/processed/openai_embeddings.json")