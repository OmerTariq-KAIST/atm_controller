"""
Card Model - Represents a bank card
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Card:
    """
    Represents a bank card with basic information.
    """
    card_number: str
    holder_name: str
    expiry_date: datetime
    card_type: str = "DEBIT"  # DEBIT, CREDIT, etc.
    is_active: bool = True
    
    def __post_init__(self):
        """Validate card data after initialization."""
        if not self.card_number or len(self.card_number) < 12:
            raise ValueError("Invalid card number")
        
        if not self.holder_name:
            raise ValueError("Cardholder name is required")
        
        if self.expiry_date < datetime.now():
            self.is_active = False
    
    def is_expired(self) -> bool:
        """Check if the card is expired."""
        return datetime.now() > self.expiry_date
    
    def mask_card_number(self) -> str:
        """Return masked card number for display purposes."""
        if len(self.card_number) < 4:
            return "*" * len(self.card_number)
        return "*" * (len(self.card_number) - 4) + self.card_number[-4:]