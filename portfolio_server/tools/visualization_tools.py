"""
Tools for visualizing portfolio data.
"""
import matplotlib.pyplot as plt
from io import BytesIO
from mcp.server.fastmcp import Image

from portfolio_server.data.storage import load_portfolio

def visualize_portfolio(user_id: str) -> Image:
    """
    Create a visualization of the current portfolio allocation
    
    Args:
        user_id: Unique identifier for the user
    """
    portfolio = load_portfolio(user_id)
    
    # Prepare data for visualization
    labels = []
    sizes = []
    colors = []
    
    # Add stocks (in blue shades)
    for i, (symbol, allocation) in enumerate(portfolio["stocks"].items()):
        labels.append(f"{symbol} ({allocation}%)")
        sizes.append(allocation)
        # Generate different blue shades
        blue_val = min(0.8, 0.3 + (i * 0.1))
        colors.append((0, 0, blue_val))
    
    # Add bonds (in green shades)
    for i, (bond_id, allocation) in enumerate(portfolio["bonds"].items()):
        labels.append(f"{bond_id} ({allocation}%)")
        sizes.append(allocation)
        # Generate different green shades
        green_val = min(0.8, 0.3 + (i * 0.1))
        colors.append((0, green_val, 0))
    
    # Create pie chart
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    plt.title(f"Portfolio Allocation for User {user_id}")
    
    # Save to bytes object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Return as MCP Image
    return Image(data=buf.getvalue(), format="png")
