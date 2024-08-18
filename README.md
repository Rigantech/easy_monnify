# pymonnify

`pymonnify` is a Python library that simplifies the interaction with the Monnify payment gateway. This library wraps around the Monnify API, allowing users to make **GET** and **POST** requests to various Monnify endpoints with ease, without needing to handle the complexities of crafting HTTP requests.

## Features
- Simple and intuitive interface for interacting with Monnify's API.
- Functions to perform common operations such as checking wallet balance, initiating transactions, and more.
- Easily extendable to add more endpoints as Monnify evolves.

## Installation

You can install this library using pip (once it's published):
```bash
pip install pymonnify
```

## Usage
### Basic setup

First, you'll need to create an instance of the Monnify class by passing your contract code and wallet account number:
```python
from pymonnify import Monnify

# Initialize the Monnify class with your contract code and wallet account number
monnify = Monnify(contract_code="your_contract_code", wallet_acc_no="your_wallet_account_number")
```
