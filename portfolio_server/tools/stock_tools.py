"""
Tools for retrieving stock data and news.
"""
import json
from typing import List, Dict, Any

from portfolio_server.api.alpha_vantage import fetch_stock_data
from portfolio_server.api.news_api import fetch_stock_news as fetch_news

async def get_stock_prices(symbols: List[str], days: int = 7) -> str:
    """
    Get recent price data for multiple stocks
    
    Args:
        symbols: List of stock symbols to fetch data for
        days: Number of days of history to include (default: 7)
    """
    result = {}
    
    for symbol in symbols:
        data = await fetch_stock_data(symbol)
        
        # Handle API errors or rate limiting
        if "Error Message" in data:
            result[symbol] = {"error": data["Error Message"]}
            continue
        
        if "Time Series (Daily)" not in data:
            result[symbol] = {"error": "No data available"}
            continue
            
        # Process the data
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
            
        result[symbol] = {
            "prices": prices,
            "percent_change": round(percent_change, 2)
        }
    
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
