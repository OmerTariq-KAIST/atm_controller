
"""
ATM Controller Usage Example
Author: Omer Tariq
Date: 2023-10-02
This script demonstrates the complete workflow of an ATM controller, including card insertion,
PIN entry, account selection, balance checking, deposits, withdrawals, and error handling.
It also showcases how to handle various exceptions that may occur during ATM operations.
This example uses mock services to simulate the behavior of an ATM system.
It is designed to be run as a standalone script for demonstration purposes.
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from atm_controller import ATMController, ATMState
from mocks.mock_bank_service import MockBankService
from mocks.mock_cash_dispenser import MockCashDispenser
from mocks.mock_card_reader import MockCardReader
from exceptions.atm_exceptions import *

import time  # might need this later for delays

def print_separator(title=""):
    """Print a visual separator."""
    print("\n" + "="*60)
    if title:
        print(f" {title} ")
        print("="*60)


def demonstrate_atm_workflow():
    """Demonstrate complete ATM workflow."""
    print_separator("ATM Controller Demonstration")
    
    # Initialize ATM with mock services
    print(" Initializing ATM Controller...")
    bank_service = MockBankService()
    cash_dispenser = MockCashDispenser(initial_cash=10000)
    card_reader = MockCardReader()
    atm = ATMController(bank_service, cash_dispenser, card_reader)
    
    print(f" ATM initialized successfully")
    print(f" ATM Cash Available: ${cash_dispenser.get_available_cash()}")
    print(f" ATM State: {atm.get_state().value}")
    
    try:
        print_separator("Card Insertion and PIN Entry")
        
        # 1. Insert card
        print(" Inserting card: 1234567890123456")
        atm.insert_card("1234567890123456")
        print(f" Card inserted successfully")
        print(f" ATM State: {atm.get_state().value}")
        
        # 2. Enter PIN
        print(" Entering PIN: 1234")
        atm.enter_pin("1234")
        print(f" PIN verified successfully")
        print(f" ATM State: {atm.get_state().value}")
        
        print_separator("Account Selection")
        
        # 3. Get available accounts
        print(" Retrieving available accounts...")
        accounts = atm.get_accounts()
        print(f" Found {len(accounts)} accounts:")
        for account in accounts:
            print(f"   • {account.account_number}: {account.account_name} "
                  f"({account.account_type.value}) - Balance: ${account.balance}")
        
        # 4. Select account
        selected_account = "1001"
        print(f"\n Selecting account: {selected_account}")
        account = atm.select_account(selected_account)
        print(f" Account selected: {account.account_name}")
        print(f" ATM State: {atm.get_state().value}")
        
        print_separator("Banking Operations")
        
        # 5. Check balance
        print(" Checking current balance...")
        balance = atm.get_balance()
        print(f" Current balance: ${balance}")
        
        # 6. Make a deposit
        deposit_amount = 500
        print(f"\n Depositing ${deposit_amount}...")
        deposit_tx = atm.deposit(deposit_amount)
        print(f"   Deposit successful!")
        print(f"   Transaction ID: {deposit_tx.transaction_id}")
        print(f"   Amount: ${deposit_tx.amount}")
        print(f"   New Balance: ${deposit_tx.balance_after}")
        print(f"   Time: {deposit_tx.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 7. Make a withdrawal
        withdraw_amount = 200
        print(f"\n Withdrawing ${withdraw_amount}...")
        withdraw_tx = atm.withdraw(withdraw_amount)
        print(f"Withdrawal successful!")
        print(f"   Transaction ID: {withdraw_tx.transaction_id}")
        print(f"   Amount: ${withdraw_tx.amount}")
        print(f"   New Balance: ${withdraw_tx.balance_after}")
        print(f"   Time: {withdraw_tx.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"ATM Cash Remaining: ${cash_dispenser.get_available_cash()}")
        
        # 8. Another deposit
        deposit_amount2 = 100
        print(f"\n Depositing ${deposit_amount2} more...")
        deposit_tx2 = atm.deposit(deposit_amount2)
        print(f"Second deposit successful! New balance: ${deposit_tx2.balance_after}")
        
        print_separator("Transaction History")
        
        # 9. View transaction history
        print("Transaction history for this session:")
        history = atm.get_transaction_history()
        for i, tx in enumerate(history, 1):
            tx_type = tx.transaction_type.value.title()
            print(f"   {i}. {tx_type}: ${tx.amount} "
                  f"(Balance: ${tx.balance_after}) "
                  f"at {tx.timestamp.strftime('%H:%M:%S')}")
        
        print(f"\n Total transactions: {len(history)}")
        total_deposited = sum(tx.amount for tx in history 
                            if tx.transaction_type.value == 'deposit')
        total_withdrawn = sum(tx.amount for tx in history 
                            if tx.transaction_type.value == 'withdrawal')
        print(f"Total deposited: ${total_deposited}")
        print(f"Total withdrawn: ${total_withdrawn}")
        print(f"Net change: ${total_deposited - total_withdrawn}")
        
        print_separator("Session Completion")
        
        # 10. Final balance check
        final_balance = atm.get_balance()
        print(f"Final account balance: ${final_balance}")
        
        # 11. Eject card
        print(" Ejecting card and ending session...")
        atm.eject_card()
        print(f"Card ejected successfully")
        print(f"ATM State: {atm.get_state().value}")
        
        print_separator("Session Summary")
        print("ATM workflow completed successfully!")
        print(f"Session duration: Complete workflow executed")
        print(f"Transactions processed: {len(history)}")
        print(f"Final balance: ${final_balance}")
        print(f"ATM ready for next customer")
        
    except InvalidCardException as e:
        print(f"❌ Invalid Card Error: {e}")
    except InvalidPinException as e:
        print(f"❌ Invalid PIN Error: {e}")
    except InsufficientFundsException as e:
        print(f"❌ Insufficient Funds Error: {e}")
    except InsufficientCashException as e:
        print(f"❌ Insufficient Cash Error: {e}")
    except AccountNotFoundException as e:
        print(f"❌ Account Not Found Error: {e}")
    except ATMException as e:
        print(f"❌ ATM Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    finally:
        # Always ensure card is ejected
        if atm.get_state() != ATMState.IDLE:
            print("🔧 Cleaning up session...")
            atm.eject_card()


def demonstrate_error_scenarios():
    """Demonstrate error handling scenarios."""
    print_separator("Error Handling Demonstration")
    
    bank_service = MockBankService()
    cash_dispenser = MockCashDispenser(initial_cash=100)  # Limited cash
    card_reader = MockCardReader()
    atm = ATMController(bank_service, cash_dispenser, card_reader)
    
    scenarios = [
        ("Invalid Card", lambda: atm.insert_card("0000000000000000")),
        ("Wrong PIN", lambda: (atm.insert_card("1234567890123456"), 
                             atm.enter_pin("0000"))),
        ("Insufficient Funds", lambda: (
            atm.insert_card("1234567890123456"),
            atm.enter_pin("1234"),
            atm.select_account("1001"),
            atm.withdraw(5000)  # More than balance
        )),
        ("Insufficient ATM Cash", lambda: (
            atm._reset_session(),
            atm.insert_card("1234567890123456"),
            atm.enter_pin("1234"),
            atm.select_account("1001"),
            atm.withdraw(200)  # More than ATM cash (100)
        )),
    ]
    
    for scenario_name, scenario_func in scenarios:
        try:
            print(f"\n Testing: {scenario_name}")
            if callable(scenario_func):
                scenario_func()
            else:
                for func in scenario_func:
                    func()
            print(f"❓ Expected error but none occurred")
        except (InvalidCardException, InvalidPinException, 
                InsufficientFundsException, InsufficientCashException) as e:
            print(f"✅ Caught expected error: {type(e).__name__}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        finally:
            atm._reset_session()


if __name__ == "__main__":
    print("Starting ATM Controller Demonstration")
    print("="*60)
    
    # Run main workflow demonstration
    demonstrate_atm_workflow()
    
    # Run error scenarios
    demonstrate_error_scenarios()
    
    print_separator("Demonstration Complete")
    print("All demonstrations completed successfully!")