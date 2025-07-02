"""
Bank Service Interface - Defines the contract for bank operations
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models.account import Account


class BankService(ABC):
    """
    Abstract interface for bank service operations.
    
    This interface defines the contract for communicating with bank systems.
    Implementations can connect to real bank APIs or provide mock services for testing.
    """
    
    @abstractmethod
    def validate_card(self, card_number: str) -> bool:
        """
        Validate if a card is valid and active.
        
        Args:
            card_number: The card number to validate
            
        Returns:
            bool: True if card is valid and active
        """
        pass
    
    @abstractmethod
    def verify_pin(self, card_number: str, pin: str) -> bool:
        """
        Verify the PIN for a given card.
        
        Args:
            card_number: The card number
            pin: The PIN to verify
            
        Returns:
            bool: True if PIN is correct
        """
        pass
    
    @abstractmethod
    def get_accounts(self, card_number: str) -> List[Account]:
        """
        Get all accounts associated with a card.
        
        Args:
            card_number: The card number
            
        Returns:
            List[Account]: List of accounts linked to the card
        """
        pass
    
    @abstractmethod
    def get_account(self, account_number: str) -> Optional[Account]:
        """
        Get account information by account number.
        
        Args:
            account_number: The account number
            
        Returns:
            Optional[Account]: Account information or None if not found
        """
        pass
    
    @abstractmethod
    def get_balance(self, account_number: str) -> int:
        """
        Get the current balance of an account.
        
        Args:
            account_number: The account number
            
        Returns:
            int: Current account balance
        """
        pass
    
    @abstractmethod
    def deposit(self, account_number: str, amount: int) -> int:
        """
        Deposit money to an account.
        
        Args:
            account_number: The account number
            amount: Amount to deposit
            
        Returns:
            int: New account balance after deposit
        """
        pass
    
    @abstractmethod
    def withdraw(self, account_number: str, amount: int) -> int:
        """
        Withdraw money from an account.
        
        Args:
            account_number: The account number
            amount: Amount to withdraw
            
        Returns:
            int: New account balance after withdrawal
            
        Raises:
            InsufficientFundsException: If account has insufficient funds
        """
        pass