from pathlib import Path
from app.ingestion.loader import load_pdf

pdf_files = list(Path("../data/raw").glob("*.pdf"))

for pdf_path in pdf_files:
    print(
        f"Processing: {pdf_path.name}"
    )

    documents = load_pdf(
        str(pdf_path)
    )

    print(
        f"Extracted {len(documents)} pages"
    )

    for document in documents:
        print(
            document.metadata,
        )

        print(
            document.text[:300]
        )
