"""
Tools for analyzing portfolio data.
"""
import json
from typing import Dict

from portfolio_server.data.storage import load_portfolio
from portfolio_server.tools.stock_tools import get_stock_prices

async def generate_portfolio_report(user_id: str) -> str:
    """
    Generate a comprehensive report on the current portfolio
    
    Args:
        user_id: Unique identifier for the user
    """
    portfolio = load_portfolio(user_id)
    
    if not portfolio["stocks"] and not portfolio["bonds"]:
        return "Portfolio is empty. Use update_portfolio tool to add investments."
    
    # Get stock price data
    stock_symbols = list(portfolio["stocks"].keys())
    price_data = json.loads(await get_stock_prices(stock_symbols))
    
    # Create a report
    report = ["# Portfolio Analysis Report", ""]
    report.append(f"## Current Allocation")
    report.append(f"- **Stocks**: {sum(portfolio['stocks'].values())}%")
    report.append(f"- **Bonds**: {sum(portfolio['bonds'].values())}%")
    report.append("")
    
    # Add performance section
    report.append("## Recent Performance")
    
    # Stock performance
    if stock_symbols:
        report.append("### Stocks")
        for symbol, allocation in portfolio["stocks"].items():
            if symbol in price_data and "percent_change" in price_data[symbol]:
                change = price_data[symbol]["percent_change"]
                contribution = (change * allocation) / 100
                report.append(f"- **{symbol}** ({allocation}% of portfolio): {change}% change, contributing {contribution:.2f}% to portfolio")
            else:
                report.append(f"- **{symbol}** ({allocation}% of portfolio): No recent data available")
        report.append("")
    
    # Bond performance (simplified as bonds have more complex data sources)
    if portfolio["bonds"]:
        report.append("### Bonds")
        report.append("Bond data typically changes less frequently than stocks.")
        for bond_id, allocation in portfolio["bonds"].items():
            report.append(f"- **{bond_id}** ({allocation}% of portfolio)")
        report.append("")
    
    # Add overall portfolio performance calculation
    # This is simplified but would be more comprehensive in a real app
    total_contribution = 0
    for symbol, allocation in portfolio["stocks"].items():
        if symbol in price_data and "percent_change" in price_data[symbol]:
            change = price_data[symbol]["percent_change"]
            contribution = (change * allocation) / 100
            total_contribution += contribution
    
    report.append(f"## Overall Portfolio Performance")
    report.append(f"The portfolio has changed approximately {total_contribution:.2f}% recently based on stock performance.")
    
    return "\n".join(report)

async def get_investment_recommendations(user_id: str) -> str:
    """
    Get personalized investment recommendations based on current portfolio
    
    Args:
        user_id: Unique identifier for the user
    """
    portfolio = load_portfolio(user_id)
    
    if not portfolio["stocks"] and not portfolio["bonds"]:
        return "Portfolio is empty. Use update_portfolio tool to add investments first."
    
    # Calculate current asset allocation
    stock_allocation = sum(portfolio["stocks"].values())
    bond_allocation = sum(portfolio["bonds"].values())
    total_allocation = stock_allocation + bond_allocation
    
    recommendations = ["# Investment Recommendations", ""]
    
    # Check portfolio diversification
    stock_count = len(portfolio["stocks"])
    if stock_count < 5 and stock_allocation > 30:
        recommendations.append("## Diversification")
        recommendations.append("Your stock portfolio appears concentrated in a small number of stocks.")
        recommendations.append("Consider adding more stocks to reduce company-specific risk.")
        recommendations.append("")
    
    # Check asset allocation
    recommendations.append("## Asset Allocation")
    if stock_allocation > 0:
        stock_percent = (stock_allocation / total_allocation) * 100
        recommendations.append(f"Current allocation: {stock_percent:.1f}% stocks, {100-stock_percent:.1f}% bonds")
        
        # Very simplified recommendation based on stock/bond ratio
        # A real application would consider age, goals, risk tolerance, etc.
        if stock_percent > 80:
            recommendations.append("Your portfolio is heavily weighted toward stocks, which increases volatility.")
            recommendations.append("Consider increasing bond allocation for more stability.")
        elif stock_percent < 30:
            recommendations.append("Your portfolio is very conservative with a high bond allocation.")
            recommendations.append("Consider increasing stock allocation for greater long-term growth potential.")
        else:
            recommendations.append("Your current stock/bond allocation appears reasonably balanced.")
    recommendations.append("")
    
    # Check for overconcentration in individual positions
    for symbol, allocation in portfolio["stocks"].items():
        if allocation > 15:  # Simplified threshold
            recommendations.append(f"**{symbol}** represents {allocation}% of your portfolio, which is relatively high.")
            recommendations.append(f"Consider reducing this position to limit single-stock risk.")
            recommendations.append("")
    
    if len(recommendations) <= 3:  # Only has the title and asset allocation
        recommendations.append("Your portfolio appears well-structured based on basic checks.")
        recommendations.append("For more detailed recommendations, consider adding more information about your financial goals and risk tolerance.")
    
    return "\n".join(recommendations)
