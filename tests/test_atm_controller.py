"""
Test Suite for ATM Controller

This comprehensive test suite verifies all ATM controller functionality
including state management, error handling, and transaction processing.
"""
import pytest
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from atm_controller import ATMController, ATMState
from models.account import Account, AccountType
from models.transaction import TransactionType
from mocks.mock_bank_service import MockBankService
from mocks.mock_cash_dispenser import MockCashDispenser
from mocks.mock_card_reader import MockCardReader
from exceptions.atm_exceptions import (
    InvalidCardException, InvalidPinException, InsufficientFundsException,
    InsufficientCashException, AccountNotFoundException, ATMException
)


class TestATMController:
    """Test cases for ATM Controller functionality."""
    
    @pytest.fixture
    def atm_controller(self):
        """Create ATM controller with mock services for testing."""
        bank_service = MockBankService()
        cash_dispenser = MockCashDispenser(initial_cash=5000)
        card_reader = MockCardReader()
        return ATMController(bank_service, cash_dispenser, card_reader)
    
    @pytest.fixture
    def reset_mocks(self, atm_controller):
        """Reset mock services to initial state before each test."""
        atm_controller._bank_service.reset_accounts()
        atm_controller._cash_dispenser.reset(5000)
        atm_controller._card_reader.eject_card()
        atm_controller._reset_session()
        yield atm_controller
    
    def test_initial_state(self, atm_controller):
        """Test ATM controller initial state."""
        assert atm_controller.get_state() == ATMState.IDLE
        assert atm_controller._current_card is None
        assert atm_controller._current_account is None
        assert len(atm_controller.get_transaction_history()) == 0
    
    def test_insert_valid_card(self, reset_mocks):
        """Test inserting a valid card."""
        atm = reset_mocks
        result = atm.insert_card("1234567890123456")
        
        assert result is True
        assert atm.get_state() == ATMState.CARD_INSERTED
        assert atm._current_card is not None
        assert atm._current_card.card_number == "1234567890123456"
    
    def test_insert_invalid_card(self, reset_mocks):
        """Test inserting an invalid card."""
        atm = reset_mocks
        
        with pytest.raises(InvalidCardException):
            atm.insert_card("3456789012345678")  # Invalid card
        
        assert atm.get_state() == ATMState.IDLE
        assert atm._current_card is None
    
    def test_insert_card_wrong_state(self, reset_mocks):
        """Test inserting card when ATM is not in idle state."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        
        with pytest.raises(ATMException):
            atm.insert_card("2345678901234567")
    
    def test_enter_correct_pin(self, reset_mocks):
        """Test entering correct PIN."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        result = atm.enter_pin("1234")
        
        assert result is True
        assert atm.get_state() == ATMState.PIN_VERIFIED
    
    def test_enter_incorrect_pin(self, reset_mocks):
        """Test entering incorrect PIN."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        
        with pytest.raises(InvalidPinException):
            atm.enter_pin("0000")
        
        assert atm.get_state() == ATMState.IDLE  # Session reset after wrong PIN
        assert atm._current_card is None
    
    def test_enter_pin_without_card(self, reset_mocks):
        """Test entering PIN without inserting card."""
        atm = reset_mocks
        
        with pytest.raises(ATMException):
            atm.enter_pin("1234")
    
    def test_get_accounts(self, reset_mocks):
        """Test getting accounts for valid card."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        
        accounts = atm.get_accounts()
        
        assert len(accounts) == 2
        account_numbers = [acc.account_number for acc in accounts]
        assert "1001" in account_numbers
        assert "1002" in account_numbers
    
    def test_get_accounts_without_pin(self, reset_mocks):
        """Test getting accounts without PIN verification."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        
        with pytest.raises(ATMException):
            atm.get_accounts()
    
    def test_select_valid_account(self, reset_mocks):
        """Test selecting a valid account."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        
        account = atm.select_account("1001")
        
        assert account.account_number == "1001"
        assert atm.get_state() == ATMState.ACCOUNT_SELECTED
        assert atm._current_account.account_number == "1001"
    
    def test_select_invalid_account(self, reset_mocks):
        """Test selecting an invalid account."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        
        with pytest.raises(AccountNotFoundException):
            atm.select_account("9999")  # Non-existent account
    
    def test_select_account_not_owned(self, reset_mocks):
        """Test selecting an account not owned by the card."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        
        with pytest.raises(AccountNotFoundException):
            atm.select_account("2001")  # Account belongs to different card
    
    def test_get_balance(self, reset_mocks):
        """Test getting account balance."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        
        balance = atm.get_balance()
        
        assert balance == 1000  # Initial balance for account 1001
    
    def test_get_balance_without_account(self, reset_mocks):
        """Test getting balance without selecting account."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        
        with pytest.raises(ATMException):
            atm.get_balance()
    
    def test_deposit_success(self, reset_mocks):
        """Test successful deposit."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        
        transaction = atm.deposit(500)
        
        assert transaction.transaction_type == TransactionType.DEPOSIT
        assert transaction.amount == 500
        assert transaction.balance_after == 1500
        assert atm.get_balance() == 1500
        assert len(atm.get_transaction_history()) == 1
    
    def test_deposit_invalid_amount(self, reset_mocks):
        """Test deposit with invalid amount."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        
        with pytest.raises(ATMException):
            atm.deposit(-100)  # Negative amount
        
        with pytest.raises(ATMException):
            atm.deposit(0)  # Zero amount
    
    def test_deposit_without_account(self, reset_mocks):
        """Test deposit without selecting account."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        
        with pytest.raises(ATMException):
            atm.deposit(100)
    
    def test_withdraw_success(self, reset_mocks):
        """Test successful withdrawal."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        
        transaction = atm.withdraw(200)
        
        assert transaction.transaction_type == TransactionType.WITHDRAWAL
        assert transaction.amount == 200
        assert transaction.balance_after == 800
        assert atm.get_balance() == 800
        assert len(atm.get_transaction_history()) == 1
    
    def test_withdraw_insufficient_funds(self, reset_mocks):
        """Test withdrawal with insufficient funds."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")  # Balance: 1000
        
        with pytest.raises(InsufficientFundsException):
            atm.withdraw(1500)  # More than balance
    
    def test_withdraw_insufficient_cash(self, reset_mocks):
        """Test withdrawal when ATM has insufficient cash."""
        atm = reset_mocks
        atm._cash_dispenser.reset(100)  # Set ATM cash to $100
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        
        with pytest.raises(InsufficientCashException):
            atm.withdraw(200)  # More than ATM cash
    
    def test_withdraw_invalid_amount(self, reset_mocks):
        """Test withdrawal with invalid amount."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        
        with pytest.raises(ATMException):
            atm.withdraw(-50)  # Negative amount
        
        with pytest.raises(ATMException):
            atm.withdraw(0)  # Zero amount
    
    def test_multiple_transactions(self, reset_mocks):
        """Test multiple transactions in one session."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        
        # Initial balance: 1000
        atm.deposit(500)      # Balance: 1500
        atm.withdraw(200)     # Balance: 1300
        atm.deposit(100)      # Balance: 1400
        
        assert atm.get_balance() == 1400
        history = atm.get_transaction_history()
        assert len(history) == 3
        assert history[0].transaction_type == TransactionType.DEPOSIT
        assert history[1].transaction_type == TransactionType.WITHDRAWAL
        assert history[2].transaction_type == TransactionType.DEPOSIT
    
    def test_eject_card(self, reset_mocks):
        """Test ejecting card and resetting session."""
        atm = reset_mocks
        atm.insert_card("1234567890123456")
        atm.enter_pin("1234")
        atm.select_account("1001")
        atm.deposit(100)
        
        result = atm.eject_card()
        
        assert result is True
        assert atm.get_state() == ATMState.IDLE
        assert atm._current_card is None
        assert atm._current_account is None
        assert len(atm.get_transaction_history()) == 0
    
    def test_complete_atm_workflow(self, reset_mocks):
        """Test complete ATM workflow from start to finish."""
        atm = reset_mocks
        
        # 1. Insert card
        assert atm.insert_card("2345678901234567") is True
        assert atm.get_state() == ATMState.CARD_INSERTED
        
        # 2. Enter PIN
        assert atm.enter_pin("5678") is True
        assert atm.get_state() == ATMState.PIN_VERIFIED
        
        # 3. Get accounts
        accounts = atm.get_accounts()
        assert len(accounts) == 1
        assert accounts[0].account_number == "2001"
        
        # 4. Select account
        account = atm.select_account("2001")
        assert account.account_number == "2001"
        assert atm.get_state() == ATMState.ACCOUNT_SELECTED
        
        # 5. Check balance
        balance = atm.get_balance()
        assert balance == 750  # Initial balance for account 2001
        
        # 6. Make deposit
        deposit_tx = atm.deposit(250)
        assert deposit_tx.amount == 250
        assert atm.get_balance() == 1000
        
        # 7. Make withdrawal
        withdraw_tx = atm.withdraw(100)
        assert withdraw_tx.amount == 100
        assert atm.get_balance() == 900
        
        # 8. Check transaction history
        history = atm.get_transaction_history()
        assert len(history) == 2
        
        # 9. Eject card
        assert atm.eject_card() is True
        assert atm.get_state() == ATMState.IDLE
    
    def test_state_transitions(self, reset_mocks):
        """Test proper state transitions throughout ATM workflow."""
        atm = reset_mocks
        
        # Start in IDLE
        assert atm.get_state() == ATMState.IDLE
        
        # Insert card -> CARD_INSERTED
        atm.insert_card("1234567890123456")
        assert atm.get_state() == ATMState.CARD_INSERTED
        
        # Enter PIN -> PIN_VERIFIED
        atm.enter_pin("1234")
        assert atm.get_state() == ATMState.PIN_VERIFIED
        
        # Select account -> ACCOUNT_SELECTED
        atm.select_account("1001")
        assert atm.get_state() == ATMState.ACCOUNT_SELECTED
        
        # Eject card -> IDLE
        atm.eject_card()
        assert atm.get_state() == ATMState.IDLE


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v"])