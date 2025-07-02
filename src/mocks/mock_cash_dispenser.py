"""
Mock Cash Dispenser - Test implementation of CashDispenser interface
"""
from interfaces.cash_dispenser import CashDispenser
from exceptions.atm_exceptions import InsufficientCashException


class MockCashDispenser(CashDispenser):
    """
    Mock implementation of CashDispenser for testing purposes.
    
    This class simulates cash dispensing operations without requiring hardware.
    """
    
    def __init__(self, initial_cash: int = 10000):
        """
        Initialize mock cash dispenser.
        
        Args:
            initial_cash: Initial amount of cash in the ATM
        """
        self._available_cash = initial_cash
        self._total_dispensed = 0
    
    def has_sufficient_cash(self, amount: int) -> bool:
        """Check if the ATM has sufficient cash for withdrawal."""
        return self._available_cash >= amount
    
    def dispense_cash(self, amount: int) -> bool:
        """
        Dispense the specified amount of cash.
        
        Args:
            amount: Amount to dispense
            
        Returns:
            bool: True if cash dispensed successfully
            
        Raises:
            InsufficientCashException: If insufficient cash is available
        """
        if amount <= 0:
            raise ValueError("Dispense amount must be positive")
        
        if not self.has_sufficient_cash(amount):
            raise InsufficientCashException(
                f"Insufficient cash in ATM. Available: ${self._available_cash}, "
                f"Requested: ${amount}"
            )
        
        self._available_cash -= amount
        self._total_dispensed += amount
        return True
    
    def get_available_cash(self) -> int:
        """Get the total amount of cash available in the ATM."""
        return self._available_cash
    
    def refill_cash(self, amount: int) -> bool:
        """
        Refill the ATM with cash (maintenance operation).
        
        Args:
            amount: Amount to add to the ATM
            
        Returns:
            bool: True if refill successful
        """
        if amount <= 0:
            raise ValueError("Refill amount must be positive")
        
        self._available_cash += amount
        return True
    
    def get_total_dispensed(self) -> int:
        """Get the total amount of cash dispensed (for testing purposes)."""
        return self._total_dispensed
    
    def reset(self, cash_amount: int = 10000):
        """Reset the cash dispenser to initial state."""
        self._available_cash = cash_amount
        self._total_dispensed = 0