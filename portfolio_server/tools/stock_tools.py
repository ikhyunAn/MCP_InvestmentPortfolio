"""
Tools for retrieving stock data and news.
"""
import json
from typing import List, Dict, Any

from portfolio_server.api.alpha_vantage import fetch_stock_data, search_company
from portfolio_server.api.news_api import fetch_stock_news as fetch_news

async def _fetch_stock_data_with_fallback(symbol: str, days: int) -> Dict[str, Any]:
    """
    Helper function to fetch stock data with company name fallback
    
    Args:
        symbol: Stock symbol or company name to fetch data for
        days: Number of days of history to include
    """
    # First try direct symbol lookup
    data = await fetch_stock_data(symbol)
    
    # If direct lookup fails, try searching by company name
    if "Error Message" in data or "Time Series (Daily)" not in data:
        search_results = await search_company(symbol)
        
        if search_results:
            # Use the first match's symbol
            best_match = search_results[0]["symbol"]
            data = await fetch_stock_data(best_match)
            
            # If data is still not available after searching
            if "Error Message" in data or "Time Series (Daily)" not in data:
                return {
                    "error": f"Stock Data Not Found. Original Query: {symbol}, Tried Symbol: {best_match}"
                }
        else:
            return {
                "error": f"No Company or stock symbol matching '{symbol}' was found."
            }
    
    # Process successful data
    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]
        dates = sorted(time_series.keys(), reverse=True)[:days]
        
        prices = {}
        for date in dates:
            prices[date] = {
                "open": float(time_series[date]["1. open"]),
                "high": float(time_series[date]["2. high"]),
                "low": float(time_series[date]["3. low"]),
                "close": float(time_series[date]["4. close"]),
                "volume": int(time_series[date]["5. volume"])
            }
        
        # Calculate change from first to last day
        if len(dates) >= 2:
            first_close = prices[dates[-1]]["close"]
            last_close = prices[dates[0]]["close"]
            percent_change = ((last_close - first_close) / first_close) * 100
        else:
            percent_change = 0
            
        return {
            "prices": prices,
            "percent_change": round(percent_change, 2)
        }
    
    return {"error": "Unable to obtain Stock Data"}

async def get_stock_prices(symbols: List[str], days: int = 7) -> str:
    """
    Get recent price data for multiple stocks
    
    Args:
        symbols: List of stock symbols or company names to fetch data for
        days: Number of days of history to include (default: 7)
    """
    result = {}
    
    for symbol in symbols:
        result[symbol] = await _fetch_stock_data_with_fallback(symbol, days)
    
    return json.dumps(result, indent=2)

async def get_stock_news(symbols: List[str], max_articles: int = 5) -> str:
    """
    Get recent news articles about stocks in the portfolio
    
    Args:
        symbols: List of stock symbols to get news for
        max_articles: Maximum number of articles to return per symbol
    """
    result = {}
    
    for symbol in symbols:
        articles = await fetch_news(symbol, max_articles)
        result[symbol] = articles
    
    return json.dumps(result, indent=2)

async def search_stocks(query: str) -> str:
    """
    Search for stocks by company name or symbol
    
    Args:
        query: Company name or symbol to search for
        
    Returns:
        JSON string containing search results with company information
    """
    results = await search_company(query)
    return json.dumps({"results": results}, indent=2)
