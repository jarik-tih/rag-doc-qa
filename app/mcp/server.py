from mcp.server.fastmcp import FastMCP

from app.mcp.tools.search import search
from app.mcp.tools.get_document_context import get_document_context

mcp = FastMCP("RAG Document QA")

mcp.add_tool(search)
mcp.add_tool(get_document_context)

if __name__ == "__main__":
    mcp.run()