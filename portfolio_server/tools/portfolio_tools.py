from typing import Dict, List, Optional
from mcp.server.fastmcp import Context
from portfolio_server.data.storage import load_portfolio, save_portfolio

def update_portfolio(user_id: str,
                     stocks: Optional[Dict[str, float]] = None,
                     bonds: Optional[Dict[str, float]] = None,
                     ctx: Context = None) -> str:
    
    portfolio = load_portfolio(user_id)

    if stocks:
        portfolio["stocks"].update(stocks)
    if bonds:
        portfolio["bonds"].update(bonds)
    
    # validate accuracy of the portfolio
    total_percent = sum(portfolio["stocks"].values()) + sum(portfolio["bonds"].values())
    if not (95 <= total_percent <= 105):
        return f"Warning: Total allocation is {total_percent}%, which is not close to 100%"
    
    save_portfolio(user_id, portfolio)

    # return the updated portfolio
    return f"Portfolio updated successfully for user {user_id}." \
           f"({len(portfolio['stocks'])} stocks, {len(portfolio['bonds'])} bonds)"

def remove_investment(user_id: str,
                      stock_symbols: Optional[List[str]] = None,
                      bond_ids: Optional[List[str]] = None) -> str:
    
    portfolio = load_portfolio(user_id)
    
    removed = []
    if stock_symbols:
        for symbol in stock_symbols:
            if symbol in portfolio["stocks"]:
                del portfolio["stocks"][symbol]
                removed.append(symbol)
    
    if bond_ids:
        for bond_id in bond_ids:
            if bond_id in portfolio["bonds"]:
                del portfolio["bonds"][bond_id]
                removed.append(bond_id)

    save_portfolio(user_id, portfolio)

    if removed:
        return f"Removed investments: {', '.join(removed)} from user {user_id}'s portfolio."
    else:
        return "No matching investments are found for removal."

