"""
Mock Bank Service - Test implementation of BankService interface
"""
from typing import List, Optional, Dict
from interfaces.bank_service import BankService
from models.account import Account, AccountType
from exceptions.atm_exceptions import InsufficientFundsException


class MockBankService(BankService):
    """
    Mock implementation of BankService for testing purposes.
    
    This class simulates bank operations without requiring external connections.
    """
    
    def __init__(self):
        """Initialize mock bank service with test data."""
        # Mock card database: card_number -> (pin, is_valid)
        self._cards = {
            "1234567890123456": ("1234", True),
            "2345678901234567": ("5678", True),
            "3456789012345678": ("9999", False),  # Invalid card
        }
        
        # Mock account database: account_number -> Account
        self._accounts = {
            "1001": Account(
                account_number="1001",
                account_type=AccountType.CHECKING,
                balance=1000,
                account_name="Primary Checking"
            ),
            "1002": Account(
                account_number="1002",
                account_type=AccountType.SAVINGS,
                balance=5000,
                account_name="Primary Savings"
            ),
            "2001": Account(
                account_number="2001",
                account_type=AccountType.CHECKING,
                balance=750,
                account_name="Business Checking"
            ),
        }
        
        # Mock card-to-accounts mapping
        self._card_accounts = {
            "1234567890123456": ["1001", "1002"],
            "2345678901234567": ["2001"],
        }
    
    def validate_card(self, card_number: str) -> bool:
        """Validate if a card is valid and active."""
        card_info = self._cards.get(card_number)
        return card_info is not None and card_info[1]
    
    def verify_pin(self, card_number: str, pin: str) -> bool:
        """Verify the PIN for a given card."""
        card_info = self._cards.get(card_number)
        if not card_info or not card_info[1]:  # Invalid or inactive card
            return False
        return card_info[0] == pin
    
    def get_accounts(self, card_number: str) -> List[Account]:
        """Get all accounts associated with a card."""
        account_numbers = self._card_accounts.get(card_number, [])
        accounts = []
        for account_num in account_numbers:
            account = self._accounts.get(account_num)
            if account:
                accounts.append(account)
        return accounts
    
    def get_account(self, account_number: str) -> Optional[Account]:
        """Get account information by account number."""
        return self._accounts.get(account_number)
    
    def get_balance(self, account_number: str) -> int:
        """Get the current balance of an account."""
        account = self._accounts.get(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found")
        return account.balance
    
    def deposit(self, account_number: str, amount: int) -> int:
        """Deposit money to an account."""
        account = self._accounts.get(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found")
        
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        account.balance += amount
        return account.balance
    
    def withdraw(self, account_number: str, amount: int) -> int:
        """Withdraw money from an account."""
        account = self._accounts.get(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found")
        
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if account.balance < amount:
            raise InsufficientFundsException("Insufficient funds in account")
        
        account.balance -= amount
        return account.balance
    
    def add_test_card(self, card_number: str, pin: str, account_numbers: List[str]):
        """Add a test card for testing purposes."""
        self._cards[card_number] = (pin, True)
        self._card_accounts[card_number] = account_numbers
    
    def add_test_account(self, account: Account):
        """Add a test account for testing purposes."""
        self._accounts[account.account_number] = account
    
    def reset_accounts(self):
        """Reset all account balances to their initial values."""
        self._accounts["1001"].balance = 1000
        self._accounts["1002"].balance = 5000
        self._accounts["2001"].balance = 750