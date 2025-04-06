"""
SSE server setup for MCP.
This module provides utilities for running the MCP server with SSE transport.
"""
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from mcp.server.sse import SseServerTransport
from portfolio_server.server import create_mcp_server

def create_sse_app(port=8080):
    """
    Create a Starlette app for SSE transport with the portfolio MCP server.
    
    Args:
        port: Port to use for the SSE server
        
    Returns:
        Starlette app configured with SSE routes
    """
    # Create the MCP server
    mcp = create_mcp_server()
    
    # Create SSE transport
    transport = SseServerTransport("/mcp/messages")
    
    # Define route handlers
    async def handle_sse(request):
        """Handle SSE connection requests"""
        async with transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp._mcp_server.run(
                streams[0],
                streams[1],
                mcp._mcp_server.create_initialization_options()
            )
    
    # Create routes
    routes = [
        Route("/mcp/sse", endpoint=handle_sse),
        Mount("/mcp/messages", app=transport.handle_post_message)
    ]
    
    # Configure middleware
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
    ]
    
    # Create the Starlette app
    return Starlette(routes=routes, middleware=middleware)

def run_sse_server(port=8080, host="0.0.0.0"):
    """
    Run the MCP server with SSE transport using uvicorn.
    
    Args:
        port: Port to run the server on
        host: Host to bind to
    """
    app = create_sse_app(port)
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_sse_server()
