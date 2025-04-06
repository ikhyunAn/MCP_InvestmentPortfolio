"""
Alpha Vantage API client for fetching stock data.
"""
import os
import httpx
from typing import Dict, Any

ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "demo")

async def fetch_stock_data(symbol: str) -> Dict[str, Any]:
    """
    Fetch stock data from Alpha Vantage API
    
    Args:
        symbol: Stock symbol to fetch data for
        
    Returns:
        Dictionary with stock price data
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return data
