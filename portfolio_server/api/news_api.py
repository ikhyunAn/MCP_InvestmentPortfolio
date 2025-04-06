"""
News API client for fetching stock news.
"""
import os
import httpx
from typing import Dict, Any, List

NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "demo")

async def fetch_stock_news(symbol: str, max_articles: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch news articles about a specific stock
    
    Args:
        symbol: Stock symbol to get news for
        max_articles: Maximum number of articles to return
        
    Returns:
        List of news article data
    """
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&sortBy=publishedAt&language=en&pageSize={max_articles}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        
        if data.get("status") != "ok":
            return [{"error": data.get("message", "Unknown error")}]
            
        articles = []
        for article in data.get("articles", [])[:max_articles]:
            articles.append({
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "description": article.get("description")
            })
            
        return articles
