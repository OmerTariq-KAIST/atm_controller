"""
Card Reader Interface - Defines the contract for card reading operations
"""
from abc import ABC, abstractmethod
from models.card import Card


class CardReader(ABC):
    """
    Abstract interface for card reading operations.
    
    This interface defines the contract for interacting with ATM card reading hardware.
    Implementations can connect to real hardware or provide mock services for testing.
    """
    
    @abstractmethod
    def read_card(self, card_number: str) -> Card:
        """
        Read card information from the inserted card.
        
        Args:
            card_number: The card number to read
            
        Returns:
            Card: Card information
            
        Raises:
            InvalidCardException: If card cannot be read or is invalid
        """
        pass
    
    @abstractmethod
    def eject_card(self) -> bool:
        """
        Eject the currently inserted card.
        
        Returns:
            bool: True if card ejected successfully
        """
        pass
    
    @abstractmethod
    def is_card_inserted(self) -> bool:
        """
        Check if a card is currently inserted.
        
        Returns:
            bool: True if card is inserted
        """
        pass