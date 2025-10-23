"""
Alpha Vantage API client for fetching stock data.
"""
import os
import httpx
from typing import Dict, Any, List

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

async def search_company(query: str) -> List[Dict[str, str]]:
    """
    Search for companies by name or symbol using Alpha Vantage API
    
    Args:
        query: Company name or symbol to search for
        
    Returns:
        List of dictionaries containing company information:
        {
            "symbol": "AAPL",
            "name": "Apple Inc",
            "type": "Equity",
            "region": "United States"
        }
    """
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_API_KEY}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        
        if "bestMatches" not in data:
            return []
            
        results = []
        for match in data["bestMatches"]:
            results.append({
                "symbol": match["1. symbol"],
                "name": match["2. name"],
                "type": match["3. type"],
                "region": match["4. region"]
            })
        
        return results
