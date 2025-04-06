"""
Portfolio data models and business logic.
"""
from typing import Dict, List, Optional, Union

class Portfolio:
    """
    Represents a user's investment portfolio.
    """
    def __init__(self, stocks: Dict[str, float] = None, bonds: Dict[str, float] = None):
        self.stocks = stocks or {}
        self.bonds = bonds or {}
    
    @property
    def stock_allocation(self) -> float:
        """Get the total percentage allocated to stocks."""
        return sum(self.stocks.values())
    
    @property
    def bond_allocation(self) -> float:
        """Get the total percentage allocated to bonds."""
        return sum(self.bonds.values())
    
    @property
    def total_allocation(self) -> float:
        """Get the total percentage allocated."""
        return self.stock_allocation + self.bond_allocation
    
    def is_valid(self) -> bool:
        """Check if the portfolio allocations sum to approximately 100%."""
        return 95 <= self.total_allocation <= 105
    
    def to_dict(self) -> Dict:
        """Convert portfolio to a dictionary representation."""
        return {
            "stocks": self.stocks,
            "bonds": self.bonds,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Portfolio':
        """Create a Portfolio instance from a dictionary."""
        return cls(
            stocks=data.get("stocks", {}),
            bonds=data.get("bonds", {})
        )
