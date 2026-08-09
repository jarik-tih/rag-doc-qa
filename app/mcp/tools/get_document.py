from pathlib import Path


DOCUMENTS_DIR = Path("data/raw")


def get_document(document_id: str) -> str:

    document_path = DOCUMENTS_DIR / f"{document_id}.pdf"

    if not document_path.exists():
        raise FileNotFoundError(
            f"Document '{document_id}' not found."
        )

    return document_path.read_text(
        encoding="utf-8"
    )