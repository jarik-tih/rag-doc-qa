import json
from pathlib import Path

def save_nodes(nodes, output_path):
    data = []
    document_counters = {}

    for node in nodes:

        document_id = node.metadata.get(
            "document_id"
        )

        if document_id not in document_counters:
            document_counters[document_id] = 0

        chunk_index = document_counters[document_id]
        document_counters[document_id] += 1

        metadata = dict(node.metadata)

        metadata["document_id"] = document_id
        metadata["chunk_index"] = chunk_index

        data.append({
            "id": node.node_id,
            "text": node.text,
            "metadata": metadata,
        })

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )

def print_stats(name, nodes):
    lengths = [len(node.text) for node in nodes]
    avg_len = sum(lengths) / len(lengths)

    print(
        f"{name}: "
        f"{len(nodes)} chunks, "
        f"avg chars={avg_len:.0f}"
    )