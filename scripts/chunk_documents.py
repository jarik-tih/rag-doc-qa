from app.ingestion.loader import load_documents
from app.ingestion.chunking import (
    fixed_chunking,
    recursive_chunking,
    semantic_chunking
)
from app.ingestion.utils import (
    save_nodes,
    print_stats
)
from pathlib import Path

documents = load_documents("../data/raw")

file_path = Path("../data/processed/fixed_nodes.json")
if file_path.is_file()==False:
    fixed_nodes = fixed_chunking(documents)
    save_nodes(fixed_nodes, "../data/processed/fixed_nodes.json")
    print_stats("Fixed Nodes", fixed_nodes)

file_path = Path("../data/processed/recursive_nodes.json")
if file_path.is_file()==False:
    recursive_nodes = recursive_chunking(documents)
    save_nodes(recursive_nodes, "../data/processed/recursive_nodes.json")
    print_stats("Recursive Nodes", recursive_nodes)

from nltk.tokenize import sent_tokenize

sentences = sent_tokenize(documents[0].text)

print(len(sentences))


file_path = Path("../data/processed/semantic_nodes.json")
if file_path.is_file()==False:
    semantic_nodes = semantic_chunking(documents)
    save_nodes(semantic_nodes, "../data/processed/semantic_nodes.json")
    print_stats("Semantic Nodes", semantic_nodes)

