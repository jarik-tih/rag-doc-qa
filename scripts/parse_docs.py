from app.ingestion.loader import load_documents

documents = load_documents("../data/raw")

print(len(documents),"loaded documents")
print(documents[0].metadata)