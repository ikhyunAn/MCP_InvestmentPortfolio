"""
MCP resources for portfolio data.
"""
import json
from typing import List

from portfolio_server.data.storage import load_portfolio
from portfolio_server.tools.stock_tools import get_stock_prices

def get_portfolio_resource(user_id: str) -> str:
    """
    Get the current portfolio data as a resource
    
    Args:
        user_id: Unique identifier for the user
    """
    portfolio = load_portfolio(user_id)
    return json.dumps(portfolio, indent=2)

async def get_portfolio_performance(user_id: str) -> str:
    """
    Get the current portfolio performance data as a resource
    
    Args:
        user_id: Unique identifier for the user
    """
    portfolio = load_portfolio(user_id)
    
    if not portfolio["stocks"]:
        return "No stocks in portfolio to analyze performance."
    
    # Get stock price data
    stock_symbols = list(portfolio["stocks"].keys())
    price_data = json.loads(await get_stock_prices(stock_symbols))
    
    # Calculate performance metrics
    performance = {
        "symbols": {},
        "total_contribution": 0
    }
    
    for symbol, allocation in portfolio["stocks"].items():
        if symbol in price_data and "percent_change" in price_data[symbol]:
            change = price_data[symbol]["percent_change"]
            contribution = (change * allocation) / 100
            performance["symbols"][symbol] = {
                "allocation": allocation,
                "percent_change": change,
                "contribution": contribution
            }
            performance["total_contribution"] += contribution
    
    return json.dumps(performance, indent=2)
