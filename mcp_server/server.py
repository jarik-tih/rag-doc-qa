from mcp.server.fastmcp import FastMCP
from mcp_server.tools.search import search
from mcp_server.tools.get_document_context import get_document_context

mcp = FastMCP(
    name = "RAG Document QA",
    host = "localhost",
    port = 8080,
)

mcp.tool()(search)
mcp.tool()(get_document_context)

if __name__ == "__main__":
    mcp.run()