# ATM Controller

A simple, extensible ATM controller implementation in Python that demonstrates clean architecture

## Features

- **Complete ATM Workflow**: Insert Card → PIN → Select Account → Balance/Deposit/Withdraw
- **Clean Architecture**: Interface-based design with dependency injection
- **Comprehensive Testing**: Full test suite
- **Error Handling**: Robust exception handling for all edge cases
- **State Management**: Proper ATM state transitions and session management

## Project Structure

```
atm-controller/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── atm_controller.py          # Main ATM controller logic
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── bank_service.py        # Bank operations interface
│   │   ├── cash_dispenser.py      # Cash dispensing interface
│   │   └── card_reader.py         # Card reading interface
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account.py             # Account model
│   │   ├── card.py                # Card model
│   │   └── transaction.py         # Transaction model
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── atm_exceptions.py      # Custom exceptions
│   └── mocks/
│       ├── __init__.py
│       ├── mock_bank_service.py   # Mock bank service for testing
│       ├── mock_cash_dispenser.py # Mock cash dispenser for testing
│       └── mock_card_reader.py    # Mock card reader for testing
└── tests/
    ├── __init__.py
    └── test_atm_controller.py      # Comprehensive test suite
```

## Architecture

The ATM Controller follows the below arch

- **ATM Controller**: Core business logic that orchestrates the ATM workflow
- **Interfaces**: Abstract contracts for external systems (bank, hardware)
- **Models**: Domain objects (Card, Account, Transaction)
- **Mock Implementations**: Test doubles for external dependencies
- **Exception Handling**: Custom exceptions for different error scenarios


## Requirements

- Python 3.8 or higher
- pytest for running tests

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd atm-controller
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

   **OR install dependencies only:**
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Method 1: Using the test runner script (Recommended)
```bash
python run_tests.py
```

### Method 2: Direct pytest with PYTHONPATH
```bash
PYTHONPATH=src pytest tests/ -v
```

### Method 3: Using pytest after installing package
```bash
pip install -e .
pytest tests/ -v
```
## Running the Demo

### Method 1: Using PYTHONPATH (Recommended)
```bash
PYTHONPATH=src python usage_example.py
```

### Method 2: After installing package
```bash
pip install -e .
python usage_example.py
```


## Test Data

The mock services include the following test data:

### Test Cards:
- **Card**: 1234567890123456, **PIN**: 1234, **Accounts**: 1001 (Checking), 1002 (Savings)
- **Card**: 2345678901234567, **PIN**: 5678, **Accounts**: 2001 (Business Checking)
- **Card**: 3456789012345678, **PIN**: 9999, **Status**: Invalid/Expired

### Test Accounts:
- **Account 1001**: Checking, Balance: $1,000
- **Account 1002**: Savings, Balance: $5,000
- **Account 2001**: Business Checking, Balance: $750

## Test Cases Covered

The test suite includes comprehensive coverage of:

✅ **Happy Path Scenarios**
- Complete ATM workflow from card insertion to transaction completion
- Multiple transaction types (deposit, withdrawal, balance inquiry)
- State transitions and session management

✅ **Error Handling**
- Invalid card insertion
- Incorrect PIN entry
- Insufficient funds
- Insufficient ATM cash
- Account not found
- Invalid transaction amounts

✅ **Edge Cases**
- Operations in wrong states
- Multiple cards/sessions
- Transaction history tracking
- Cash dispenser limits

✅ **Security**
- PIN verification
- Account ownership validation
- Session isolation

## Future Enhancements

This design supports easy integration of:

- **Real Bank APIs**: Replace MockBankService with actual bank integration
- **Additional Features**: Transaction limits, receipts, multiple card types
- **Security Enhancements**: Card encryption, transaction signing
- **Monitoring**: Logging, metrics, alerts
- **UI Integration**: REST API, mobile app, web interface

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please open an issue in the repository.