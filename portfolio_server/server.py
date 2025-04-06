import sys

from mcp.server.fastmcp import FastMCP
from portfolio_server.tools import portfolio_tools, stock_tools, analysis_tools, visualization_tools
from portfolio_server.resources import portfolio_resources

def create_mcp_server() -> FastMCP:
    # Create and configure the MCP server with default transport (stdio)
    try:
        print("Initializing Portfolio Manager MCP Server...", file=sys.stderr)
        mcp = FastMCP("Portfolio Manager MCP Server",
                      dependencies = [
                          "pandas",
                          "httpx",
                          "matplotlib"
                      ])
        
        # Register tools
        print("Registering tools...", file=sys.stderr)
        register_tools(mcp)
        print("Registering resources...", file=sys.stderr)
        register_resources(mcp)
        
        print("MCP Server initialized successfully!", file=sys.stderr)
        return mcp
    except Exception as e:
        print(f"ERROR initializing MCP server: {str(e)}", file=sys.stderr)
        print(f"Error type: {type(e)}", file=sys.stderr)
        # Re-raise the exception so it's visible in the logs
        raise

def register_tools(mcp: FastMCP) -> None:
    # TODO: Register all tools
    mcp.tool()(portfolio_tools.update_portfolio)
    mcp.tool()(portfolio_tools.remove_investment)
    
    mcp.tool()(stock_tools.get_stock_prices)
    mcp.tool()(stock_tools.get_stock_news)

    mcp.tool()(analysis_tools.generate_portfolio_report)
    mcp.tool()(analysis_tools.get_investment_recommendations)

    mcp.tool()(visualization_tools.visualize_portfolio)

def register_resources(mcp: FastMCP) -> None:
    # Register all resources within the portfolio_resources module
    mcp.resource("portfolio://{user_id}")(portfolio_resources.get_portfolio_resource)
    mcp.resource("portfolio-performance://{user_id}")(portfolio_resources.get_portfolio_performance)