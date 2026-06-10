import json
from pathlib import Path

def save_nodes(nodes, output_path):
    data = []
    for node in nodes:
       data.append({
           "id": node.node_id,
           "text": node.text,
           "metadata": node.metadata,
        })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(data, f,ensure_ascii=False, indent=2)

def print_stats(name, nodes):
    lengths = [len(node.text) for node in nodes]
    avg_len = sum(lengths) / len(lengths)

    print(
        f"{name}: "
        f"{len(nodes)} chunks, "
        f"avg chars={avg_len:.0f}"
    )