"""
ATM Exceptions - Custom exceptions for ATM operations
"""


class ATMException(Exception):
    """Base exception for all ATM-related errors."""
    pass


class InvalidCardException(ATMException):
    """Raised when a card is invalid or cannot be read."""
    pass


class InvalidPinException(ATMException):
    """Raised when an incorrect PIN is entered."""
    pass


class AccountNotFoundException(ATMException):
    """Raised when a requested account cannot be found."""
    pass


class InsufficientFundsException(ATMException):
    """Raised when an account has insufficient funds for a transaction."""
    pass


class InsufficientCashException(ATMException):
    """Raised when the ATM has insufficient cash for a withdrawal."""
    pass


class TransactionLimitExceededException(ATMException):
    """Raised when a transaction exceeds daily or other limits."""
    pass


class ATMMaintenanceException(ATMException):
    """Raised when ATM is under maintenance."""
    pass