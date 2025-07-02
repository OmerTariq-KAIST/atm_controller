"""
ATM Controller - Main business logic for ATM operations
"""
from enum import Enum
from typing import Optional, List
from interfaces.bank_service import BankService
from interfaces.cash_dispenser import CashDispenser
from interfaces.card_reader import CardReader
from models.card import Card
from models.account import Account
from models.transaction import Transaction, TransactionType
from exceptions.atm_exceptions import (
    InvalidCardException,
    InvalidPinException,
    InsufficientFundsException,
    InsufficientCashException,
    AccountNotFoundException,
    ATMException
)


class ATMState(Enum):
    IDLE = "idle"
    CARD_INSERTED = "card_inserted"
    PIN_VERIFIED = "pin_verified"
    ACCOUNT_SELECTED = "account_selected"


class ATMController:
    """
    Main ATM Controller that manages the ATM workflow and state.
    
    This controller is designed to be independent of specific implementations
    of bank systems, cash dispensers, and card readers, making it testable
    and extensible for future integrations.
    """
    
    def __init__(self, bank_service: BankService, cash_dispenser: CashDispenser, 
                 card_reader: CardReader):
        """
        Initialize ATM Controller with required services.
        
        Args:
            bank_service: Service for bank operations (PIN validation, account access)
            cash_dispenser: Service for cash dispensing operations
            card_reader: Service for card reading operations
        """
        self._bank_service = bank_service
        self._cash_dispenser = cash_dispenser
        self._card_reader = card_reader
        self._state = ATMState.IDLE
        self._current_card: Optional[Card] = None
        self._current_account: Optional[Account] = None
        self._transaction_history: List[Transaction] = []
    
    def get_state(self) -> ATMState:
        """Get current ATM state."""
        return self._state
    
    def insert_card(self, card_number: str) -> bool:
        """
        Insert a card into the ATM.
        
        Args:
            card_number: The card number to insert
            
        Returns:
            bool: True if card is valid and inserted successfully
            
        Raises:
            InvalidCardException: If card is invalid
            ATMException: If ATM is not in idle state
        """
        if self._state != ATMState.IDLE:
            raise ATMException("ATM is not ready to accept a card")
        
        try:
            # Validate card with bank service
            if not self._bank_service.validate_card(card_number):
                raise InvalidCardException("Invalid card")
            
            # Read card information
            card = self._card_reader.read_card(card_number)
            self._current_card = card
            self._state = ATMState.CARD_INSERTED
            return True
            
        except Exception as e:
            self._reset_session()
            raise e
    
    def enter_pin(self, pin: str) -> bool:
        """
        Enter PIN for the inserted card.
        
        Args:
            pin: The PIN to verify
            
        Returns:
            bool: True if PIN is correct
            
        Raises:
            InvalidPinException: If PIN is incorrect
            ATMException: If no card is inserted
        """
        if self._state != ATMState.CARD_INSERTED:
            raise ATMException("No card inserted or PIN already verified")
        
        if not self._current_card:
            raise ATMException("No card information available")
        
        try:
            # Verify PIN with bank service
            if not self._bank_service.verify_pin(self._current_card.card_number, pin):
                raise InvalidPinException("Incorrect PIN")
            
            self._state = ATMState.PIN_VERIFIED
            return True
            
        except InvalidPinException:
            self._reset_session()
            raise
    
    def get_accounts(self) -> List[Account]:
        """
        Get list of accounts associated with the current card.
        
        Returns:
            List[Account]: List of available accounts
            
        Raises:
            ATMException: If PIN is not verified
        """
        if self._state != ATMState.PIN_VERIFIED:
            raise ATMException("PIN not verified")
        
        if not self._current_card:
            raise ATMException("No card information available")
        
        return self._bank_service.get_accounts(self._current_card.card_number)
    
    def select_account(self, account_number: str) -> Account:
        """
        Select an account for transactions.
        
        Args:
            account_number: The account number to select
            
        Returns:
            Account: The selected account information
            
        Raises:
            AccountNotFoundException: If account is not found
            ATMException: If PIN is not verified
        """
        if self._state != ATMState.PIN_VERIFIED:
            raise ATMException("PIN not verified")
        
        if not self._current_card:
            raise ATMException("No card information available")
        
        # Get account information from bank service
        account = self._bank_service.get_account(account_number)
        if not account:
            raise AccountNotFoundException(f"Account {account_number} not found")
        
        # Verify account belongs to this card
        accounts = self._bank_service.get_accounts(self._current_card.card_number)
        if account_number not in [acc.account_number for acc in accounts]:
            raise AccountNotFoundException("Account does not belong to this card")
        
        self._current_account = account
        self._state = ATMState.ACCOUNT_SELECTED
        return account
    
    def get_balance(self) -> int:
        """
        Get the current account balance.
        
        Returns:
            int: Current account balance
            
        Raises:
            ATMException: If no account is selected
        """
        if self._state != ATMState.ACCOUNT_SELECTED:
            raise ATMException("No account selected")
        
        if not self._current_account:
            raise ATMException("No account information available")
        
        # Get fresh balance from bank service
        balance = self._bank_service.get_balance(self._current_account.account_number)
        self._current_account.balance = balance
        return balance
    
    def deposit(self, amount: int) -> Transaction:
        """
        Deposit money to the selected account.
        
        Args:
            amount: Amount to deposit (must be positive)
            
        Returns:
            Transaction: Transaction record
            
        Raises:
            ATMException: If no account is selected or invalid amount
        """
        if self._state != ATMState.ACCOUNT_SELECTED:
            raise ATMException("No account selected")
        
        if not self._current_account:
            raise ATMException("No account information available")
        
        if amount <= 0:
            raise ATMException("Deposit amount must be positive")
        
        # Process deposit through bank service
        new_balance = self._bank_service.deposit(self._current_account.account_number, amount)
        
        # Create transaction record
        transaction = Transaction(
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            account_number=self._current_account.account_number,
            balance_after=new_balance
        )
        
        self._transaction_history.append(transaction)
        self._current_account.balance = new_balance
        
        return transaction
    
    def withdraw(self, amount: int) -> Transaction:
        """
        Withdraw money from the selected account.
        
        Args:
            amount: Amount to withdraw (must be positive)
            
        Returns:
            Transaction: Transaction record
            
        Raises:
            InsufficientFundsException: If account has insufficient funds
            InsufficientCashException: If ATM has insufficient cash
            ATMException: If no account is selected or invalid amount
        """
        if self._state != ATMState.ACCOUNT_SELECTED:
            raise ATMException("No account selected")
        
        if not self._current_account:
            raise ATMException("No account information available")
        
        if amount <= 0:
            raise ATMException("Withdrawal amount must be positive")
        
        # Check if ATM has sufficient cash
        if not self._cash_dispenser.has_sufficient_cash(amount):
            raise InsufficientCashException("ATM has insufficient cash")
        
        # Check account balance
        current_balance = self.get_balance()
        if current_balance < amount:
            raise InsufficientFundsException("Insufficient funds in account")
        
        # Process withdrawal through bank service
        new_balance = self._bank_service.withdraw(self._current_account.account_number, amount)
        
        # Dispense cash
        self._cash_dispenser.dispense_cash(amount)
        
        # Create transaction record
        transaction = Transaction(
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount,
            account_number=self._current_account.account_number,
            balance_after=new_balance
        )
        
        self._transaction_history.append(transaction)
        self._current_account.balance = new_balance
        
        return transaction
    
    def get_transaction_history(self) -> List[Transaction]:
        """
        Get transaction history for current session.
        
        Returns:
            List[Transaction]: List of transactions performed in this session
        """
        return self._transaction_history.copy()
    
    def eject_card(self) -> bool:
        """
        Eject the card and reset ATM session.
        
        Returns:
            bool: True if card ejected successfully
        """
        if self._current_card:
            self._card_reader.eject_card()
        
        self._reset_session()
        return True
    
    def _reset_session(self):
        """Reset ATM session to idle state."""
        self._state = ATMState.IDLE
        self._current_card = None
        self._current_account = None
        self._transaction_history = []