"""
Mock Card Reader - Test implementation of CardReader interface
"""
from datetime import datetime, timedelta
from interfaces.card_reader import CardReader
from models.card import Card
from exceptions.atm_exceptions import InvalidCardException


class MockCardReader(CardReader):
    """
    Mock implementation of CardReader for testing purposes.
    
    This class simulates card reading operations without requiring hardware.
    """
    
    def __init__(self):
        """Initialize mock card reader."""
        self._card_inserted = False
        self._current_card = None
        
        # Mock card database for card information
        self._card_info = {
            "1234567890123456": {
                "holder_name": "John Doe",
                "expiry_date": datetime.now() + timedelta(days=365),
                "card_type": "DEBIT"
            },
            "2345678901234567": {
                "holder_name": "Jane Smith",
                "expiry_date": datetime.now() + timedelta(days=730),
                "card_type": "CREDIT"
            },
            "3456789012345678": {
                "holder_name": "Invalid User",
                "expiry_date": datetime.now() - timedelta(days=30),  # Expired
                "card_type": "DEBIT"
            },
        }
    
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
        if not card_number:
            raise InvalidCardException("No card number provided")
        
        card_info = self._card_info.get(card_number)
        if not card_info:
            raise InvalidCardException("Card not recognized")
        
        try:
            card = Card(
                card_number=card_number,
                holder_name=card_info["holder_name"],
                expiry_date=card_info["expiry_date"],
                card_type=card_info["card_type"]
            )
            
            # Check if card is expired or inactive
            if card.is_expired():
                raise InvalidCardException("Card is expired")
            
            self._card_inserted = True
            self._current_card = card
            return card
            
        except (ValueError, KeyError) as e:
            raise InvalidCardException(f"Error reading card: {str(e)}")
    
    def eject_card(self) -> bool:
        """
        Eject the currently inserted card.
        
        Returns:
            bool: True if card ejected successfully
        """
        self._card_inserted = False
        self._current_card = None
        return True
    
    def is_card_inserted(self) -> bool:
        """
        Check if a card is currently inserted.
        
        Returns:
            bool: True if card is inserted
        """
        return self._card_inserted
    
    def get_current_card(self) -> Card:
        """Get the currently inserted card (for testing purposes)."""
        return self._current_card
    
    def add_test_card(self, card_number: str, holder_name: str, 
                      expiry_date: datetime = None, card_type: str = "DEBIT"):
        """Add a test card for testing purposes."""
        if expiry_date is None:
            expiry_date = datetime.now() + timedelta(days=365)
        
        self._card_info[card_number] = {
            "holder_name": holder_name,
            "expiry_date": expiry_date,
            "card_type": card_type
        }