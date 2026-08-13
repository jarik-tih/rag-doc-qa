import fitz
from pathlib import Path
from llama_index.core import Document

def load_pdf(pdf_path: Path) -> Document:

    pdf = fitz.open(pdf_path)

    pages = []

    for page in pdf:
        text = page.get_text("text").strip()

        if text:
            pages.append(text)

    pdf.close()

    full_text = "\n\n".join(pages)

    return Document(
        text=full_text,
        metadata={
            "document_id": pdf_path.stem,
            "file_name": pdf_path.name,
            "file_path": str(pdf_path),
            "file_type": "application/pdf",
        },
    )


def load_documents(data_dir: str) -> list[Document]:

    data_path = Path(data_dir)

    documents = []

    pdf_files = sorted(
        data_path.glob("*.pdf")
    )

    for pdf_path in pdf_files:

        document = load_pdf(pdf_path)

        documents.append(document)

    return documents