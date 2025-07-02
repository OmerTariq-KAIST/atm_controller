"""
Transaction Model - Represents a transaction record
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid


class TransactionType(Enum):
    """Types of transactions."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BALANCE_INQUIRY = "balance_inquiry"


@dataclass
class Transaction:
    """
    Represents a transaction with all relevant details.
    """
    transaction_type: TransactionType
    amount: int
    account_number: str
    balance_after: int
    transaction_id: str = None
    timestamp: datetime = None
    
    def __post_init__(self):
        """Initialize transaction with default values."""
        if self.transaction_id is None:
            self.transaction_id = str(uuid.uuid4())
        
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary for serialization."""
        return {
            'transaction_id': self.transaction_id,
            'transaction_type': self.transaction_type.value,
            'amount': self.amount,
            'account_number': self.account_number,
            'balance_after': self.balance_after,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation of transaction."""
        return (f"Transaction {self.transaction_id}: "
                f"{self.transaction_type.value.title()} ${self.amount} "
                f"on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")