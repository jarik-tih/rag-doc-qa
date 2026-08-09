from mcp.server.fastmcp import FastMCP

from app.mcp.tools.search import search_documents
from app.mcp.tools.get_document import get_document

mcp = FastMCP("RAG Document QA")


@mcp.tool()
def search(
    query: str,
    top_k: int = 5,
) -> list:
    """
    Search documents using semantic vector search.
    Returns the most relevant document chunks
    from the Qdrant vector database.
    """

    return search_documents(
        query=query,
        top_k=top_k,
    )

@mcp.tool()
def get_document(
    document_id: str,
) -> str:
    """
    Return the full text of a document
    by its document ID.
    """

    return get_document(
        document_id
    )

if __name__ == "__main__":
    mcp.run()