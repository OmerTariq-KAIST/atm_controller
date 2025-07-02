"""
Cash Dispenser Interface - Defines the contract for cash dispensing operations
"""
from abc import ABC, abstractmethod


class CashDispenser(ABC):
    """
    Abstract interface for cash dispensing operations.
    
    This interface defines the contract for interacting with ATM cash dispensing hardware.
    Implementations can connect to real hardware or provide mock services for testing.
    """
    
    @abstractmethod
    def has_sufficient_cash(self, amount: int) -> bool:
        """
        Check if the ATM has sufficient cash for withdrawal.
        
        Args:
            amount: Amount to check
            
        Returns:
            bool: True if sufficient cash is available
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_available_cash(self) -> int:
        """
        Get the total amount of cash available in the ATM.
        
        Returns:
            int: Total available cash amount
        """
        pass
    
    @abstractmethod
    def refill_cash(self, amount: int) -> bool:
        """
        Refill the ATM with cash (maintenance operation).
        
        Args:
            amount: Amount to add to the ATM
            
        Returns:
            bool: True if refill successful
        """
        pass