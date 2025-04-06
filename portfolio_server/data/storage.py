"""
Storage utilities for portfolio data.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any

# Setup storage paths
PORTFOLIO_DIR = os.path.expanduser("~/.portfolio-manager")
os.makedirs(PORTFOLIO_DIR, exist_ok=True)

def get_portfolio_path(user_id: str) -> str:
    """
    Get the path to a user's portfolio file.
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        Path to the portfolio JSON file
    """
    return os.path.join(PORTFOLIO_DIR, f"{user_id}_portfolio.json")

def load_portfolio(user_id: str) -> Dict[str, Any]:
    """
    Load a user's portfolio, or return empty one if none exists.
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        Portfolio data including stocks and bonds
    """
    path = get_portfolio_path(user_id)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {"stocks": {}, "bonds": {}, "last_updated": None}

def save_portfolio(user_id: str, portfolio: Dict[str, Any]) -> None:
    """
    Save a user's portfolio to disk.
    
    Args:
        user_id: Unique identifier for the user
        portfolio: Portfolio data to save
    """
    portfolio["last_updated"] = datetime.now().isoformat()
    with open(get_portfolio_path(user_id), 'w') as f:
        json.dump(portfolio, f, indent=2)
