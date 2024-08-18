# pymonnify

`pymonnify` is a Python library that simplifies the interaction with the Monnify payment gateway. This library wraps around the Monnify API, allowing users to make **GET** and **POST** requests to various Monnify endpoints with ease, without needing to handle the complexities of crafting HTTP requests.

## Features
- Simple and intuitive interface for interacting with Monnify's API.
- Functions to perform common operations such as checking wallet balance, initiating transactions, and more.
- Easily extendable to add more endpoints as Monnify evolves.

## Registration
To use this library effectively, ensure you have created an account with monnify. if not, kindly create an account here [https://app.monnify.com/create-account](https://app.monnify.com/create-account)

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

# Initialize the Monnify class with your API key, Client Secret Key and Environment
monnify = Monnify(apiKey="your_api_key", clientSecretKey="your_client_secret_key", environment="live")
# environment can either be "live" for production or "sandbox" for development.
# If no environment is specified, it defaults to "live"
```

### Available Functions

<table>
    <thead>
        <tr>
            <th>Category</th>
            <th>Functions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Reserved Accounts<td>
            <td>
                - Create Reserved Account (Invoice)<br>
                - Create Reserved Account (General)<br>
                - Get Reserved Account Details<br>
                - Delete Reserved Accounts<br>
                - Add Linked Accounts<br>
                - Update BVN for Reserved Account
            </td>
        </tr>
        <tr>
            <td>Transactions<td>
            <td>
                - Initiate A Transaction
                - Pay With Bank Transfer
                - Pay With Card
                - Authroize OTP
                - Get Transactions For A Reserved Account
                - Get All Transactions / Search Transactions
                - Get A Transaction Details
            </td>
        </tr>
        <tr>
            <td>Sub Accounts<td>
            <td>
                - Create Sub Account
                - Delete Sub Account
                - Get All Sub Accounts
                - Update A Sub Account Info
                - Update Split Config For A Reserved Account
            </td>
        </tr>
        <tr>
            <td>Transfers<td>
            <td>
                - Initiate A Single Transfer
                - Authorize A Transfer / Validate OTP
                - Resend OTP
                - Get Transfer Status
                - Search Transfers
                - Get All Transfers
            </td>
        </tr>
        <tr>
            <td>Wallet Account<td>
            <td>
                - Get Wallet Balance
                - Get List of Banks (supported by Monnify) [See sample list](src/assets/banks.json)
                - Get All Available Bank USSDs (supported by Monnify) [See sample list](src/assets/banks_ussd.json)
            </td>
        </tr>
    </tbody>
</table>