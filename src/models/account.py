"""
Account Model - Represents a bank account
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AccountType(Enum):
    """Types of bank accounts."""
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"


@dataclass
class Account:
    """
    Represents a bank account with basic information.
    """
    account_number: str
    account_type: AccountType
    balance: int
    account_name: str
    is_active: bool = True
    daily_withdrawal_limit: Optional[int] = None
    
    def __post_init__(self):
        """Validate account data after initialization."""
        if not self.account_number:
            raise ValueError("Account number is required")
        
        if not self.account_name:
            raise ValueError("Account name is required")
        
        # Set default daily withdrawal limit if not specified
        if self.daily_withdrawal_limit is None:
            if self.account_type == AccountType.CHECKING:
                self.daily_withdrawal_limit = 1000
            elif self.account_type == AccountType.SAVINGS:
                self.daily_withdrawal_limit = 500
            else:  # CREDIT
                self.daily_withdrawal_limit = 300
    
    def can_withdraw(self, amount: int) -> bool:
        """
        Check if withdrawal amount is allowed.
        
        Args:
            amount: Amount to check
            
        Returns:
            bool: True if withdrawal is allowed
        """
        if not self.is_active:
            return False
        
        if amount <= 0:
            return False
        
        if self.daily_withdrawal_limit and amount > self.daily_withdrawal_limit:
            return False
        
        # For credit accounts, balance can be negative up to credit limit
        if self.account_type == AccountType.CREDIT:
            # Assuming negative balance represents available credit
            return True
        
        return self.balance >= amount
    
    def mask_account_number(self) -> str:
        """Return masked account number for display purposes."""
        if len(self.account_number) < 4:
            return "*" * len(self.account_number)
        return "*" * (len(self.account_number) - 4) + self.account_number[-4:]