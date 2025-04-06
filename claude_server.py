#!/usr/bin/env python3
"""
Simplified portfolio manager MCP server for Claude Desktop.
Designed with minimal dependencies to maximize compatibility.
"""
import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Optional

try:
    import mcp
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: MCP package not found. Please install it with: pip install mcp[cli]", file=sys.stderr)
    sys.exit(1)

print(f"Python version: {sys.version}", file=sys.stderr)
print(f"MCP version: {mcp.__version__ if hasattr(mcp, '__version__') else 'unknown'}", file=sys.stderr)
print(f"Current directory: {os.getcwd()}", file=sys.stderr)

# Create the MCP server
mcp_server = FastMCP("Portfolio Manager")

# Setup basic storage
PORTFOLIO_DIR = os.path.expanduser("~/.portfolio-manager")
os.makedirs(PORTFOLIO_DIR, exist_ok=True)

def get_portfolio_path(user_id: str) -> str:
    return os.path.join(PORTFOLIO_DIR, f"{user_id}_portfolio.json")

def load_portfolio(user_id: str) -> Dict:
    path = get_portfolio_path(user_id)
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {path}", file=sys.stderr)
            return {"stocks": {}, "bonds": {}, "last_updated": None}
    return {"stocks": {}, "bonds": {}, "last_updated": None}

def save_portfolio(user_id: str, portfolio: Dict) -> None:
    portfolio["last_updated"] = datetime.now().isoformat()
    path = get_portfolio_path(user_id)
    with open(path, 'w') as f:
        json.dump(portfolio, f, indent=2)

# Define basic tools
@mcp_server.tool()
def update_portfolio(user_id: str, 
                     stocks: Optional[Dict[str, float]] = None,
                     bonds: Optional[Dict[str, float]] = None) -> str:
    """
    Update a user's investment portfolio
    
    Args:
        user_id: Unique identifier for the user
        stocks: Dictionary of stock symbols to allocation percentage (e.g. {"AAPL": 10.5, "MSFT": 15.0})
        bonds: Dictionary of bond identifiers to allocation percentage (e.g. {"US10Y": 30.0, "CORP_AAA": 20.0})
    """
    portfolio = load_portfolio(user_id)
    
    if stocks:
        portfolio["stocks"].update(stocks)
    
    if bonds:
        portfolio["bonds"].update(bonds)
    
    # Validate that percentages sum to approximately 100%
    total_pct = sum(portfolio["stocks"].values()) + sum(portfolio["bonds"].values())
    if not (95 <= total_pct <= 105):
        return f"Warning: Total allocation is {total_pct}%, which is not close to 100%"
    
    save_portfolio(user_id, portfolio)
    
    # Return a summary of the updated portfolio
    return f"Portfolio updated for user {user_id}. Current allocation: {total_pct}% allocated " \
           f"({len(portfolio['stocks'])} stocks, {len(portfolio['bonds'])} bonds)"

@mcp_server.tool()
def view_portfolio(user_id: str) -> str:
    """
    View a user's current portfolio allocation
    
    Args:
        user_id: Unique identifier for the user
    """
    portfolio = load_portfolio(user_id)
    
    if not portfolio["stocks"] and not portfolio["bonds"]:
        return "Portfolio is empty. Use update_portfolio tool to add investments."
    
    result = ["# Current Portfolio Allocation", ""]
    
    # Add stocks
    if portfolio["stocks"]:
        result.append("## Stocks")
        for symbol, allocation in portfolio["stocks"].items():
            result.append(f"- {symbol}: {allocation}%")
        result.append("")
    
    # Add bonds
    if portfolio["bonds"]:
        result.append("## Bonds")
        for bond_id, allocation in portfolio["bonds"].items():
            result.append(f"- {bond_id}: {allocation}%")
        result.append("")
    
    # Add totals
    stock_allocation = sum(portfolio["stocks"].values())
    bond_allocation = sum(portfolio["bonds"].values())
    total_allocation = stock_allocation + bond_allocation
    
    result.append(f"## Summary")
    result.append(f"- Total stock allocation: {stock_allocation}%")
    result.append(f"- Total bond allocation: {bond_allocation}%")
    result.append(f"- Total allocation: {total_allocation}%")
    
    return "\n".join(result)

@mcp_server.resource("portfolio://{user_id}")
def get_portfolio_resource(user_id: str) -> str:
    """
    Get the current portfolio data as a resource
    
    Args:
        user_id: Unique identifier for the user
    """
    portfolio = load_portfolio(user_id)
    return json.dumps(portfolio, indent=2)

if __name__ == "__main__":
    print("Portfolio Manager MCP Server starting with simplified configuration...", file=sys.stderr)
    mcp_server.run()
