.# easy_monnify

`easy_monnify` is a Python library that simplifies the interaction with the Monnify payment gateway. This library wraps around the Monnify API, allowing users to make **GET** and **POST** requests to various Monnify endpoints with ease, without needing to handle the complexities of crafting HTTP requests.

## Features
- Simple and intuitive interface for interacting with Monnify's API.
- Functions to perform common operations such as checking wallet balance, initiating transactions, and more.
- Easily extendable to add more endpoints as Monnify evolves.

## Registration
To use this library effectively, ensure you have created an account with monnify. if not, kindly create an account here [https://app.monnify.com/create-account](https://app.monnify.com/create-account)

## Installation

You can install this library using pip (once it's published):
```bash
pip install easy_monnify
```

## Usage
### Basic setup

First, you'll need to create an instance of the Monnify class by passing your contract code and wallet account number:
```python
from  easy_monnify import Monnify

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
            <td>Reserved Accounts</td>
            <td>
                <ul>
                    <li>Create Reserved Account</li>
                    <li>Get Reserved Account Details</li>
                    <li>Delete Reserved Accounts</li>
                    <li>Update BVN for Reserved Account</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Transactions</td>
            <td>
                <ul>
                    <li>Initiate A Transaction</li>
                    <li>Pay With Bank Transfer</li>
                    <li>Webhook Notification</li>
                    <li>Settlement Notification</li>
                    <li>Get A Transaction Details/ Verify Transaction</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Invoice Transactions (coming soon)</td>
            <td>
                <ul>
                    <li>Create Invoice</li>
                    <li>Get Invoice Details</li>
                    <li>Get All Invoice</li>
                    <li>Reserved Account Invoices</li>
                    <li>Webhook Notifications</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Sub Accounts/ Split Settlements</td>
            <td>
                <ul>
                    <li>Create Sub Account</li>
                    <li>Get All Sub Accounts</li>
                    <li>Update A Sub Account Info</li>
                    <li>Delete Sub Account</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Limit Transactions (coming soon)</td>
            <td>
                <ul>
                    <li>Create Limit Profile</li>
                    <li>Update Limit Profile</li>
                    <li>Get Limit Profiles</li>
                    <li>Reserve Account with Limit</li>
                    <li>Update A Reserve Account Limit</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Disbursement Transactions / Transfers</td>
            <td>
                <ul>
                    <li>Initiate A Single Transfer</li>
                    <li>Initiate A Bulk Transfer</li>
                    <li>Authorize A Single Transfer / Validate OTP</li>
                    <li>Authorize Bulk Transfer / Validate OTP</li>
                    <li>Resend OTP</li>
                    <li>Get Single Transfer Status</li>
                    <li>Get Bulk Transfer Status</li>
                    <li>Get All Transfers</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Wallet Account (coming soon)</td>
            <td>
                <ul>
                    <li>Get Wallet Balance</li>
                    <li>Get List of Banks (supported by Monnify) <a href="https://github.com/Rigantech/easy_monnify/blob/main/src/assets/banks.json">See sample list</a></li>
                    <li>Get All Available Bank USSDs (supported by Monnify) <a href="https://github.com/Rigantech/easy_monnify/blob/main/src/assets/banks_ussd.json">See sample list</a></li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Bank Verification</td>
            <td>
                <ul>
                    <li>Verify Bank Account</li>
                    <li>Verify BVN Number (with Date of Birth)</li>
                    <li>Verify BVN Number (with Bank Account)</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

### Usage

### Reserved Accounts
Reserved account APIs enable merchants create accounts that can be dedicated to each of their customers. Once any payment is done to that account, we notify your webhook with the payment information.
- Create Reserved Account
    ```python
    data = monnify.createReservedAccount(
        accountReference="reference_to_the_account", # generated by you to identify the account
        accountName="name_of_account.",
        currencyCode="NGN", # currency is in Naira
        contractCode="your_monnify_account_contract_code",- # see Monnify dashboard
        customerName="name_of_customer",
        customerEmail="email_of_customer",
    )
    print(data)
    ```
    - ```accountReference:``` String, Required
    - ```accountName:``` String, Required
    - ```currencyCode:``` String, Required, should be "NGN"
    - ```contractCode:``` String, Required
    - ```customerName:``` String, Required
    - ```customerEmail:``` String, Required

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "contractCode": "4876165459",
            "accountReference": "jsnow1234",
            "accountName": "John Snow Limited",
            "currencyCode": "NGN",
            "customerEmail": "john@snow.com",
            "customerName": "John Snow Limited",
            "accountNumber": "9879377424",
            "bankName": "Providus Bank",
            "bankCode": "101",
            "status": "ACTIVE",
            "createdOn": "2019-12-08 15:52:04.726",
            "incomeSplitConfig": []
        }
    }
    ```
    #### sample response - error
    ```bash
    # status 400
    {
        "requestSuccessful": false,
        "responseMessage": "Field contractCode cannot be null",
        "responseCode": "99"
    }

    # status 401
    {
        "error": "invalid_token",
        "error_description": "Access token expired: -geneerated_access_token"
    }

    # status 422
    {
        "requestSuccessful": false,
        "responseMessage": "You can not reserve two accounts with the same reference",
        "responseCode": "99"
    }
    ```

- Get Reserved Account Details
    ```python
    data = monnify.getReservedAccountDetails(
        accountReference="reference_to_the_account"
    )
    print(data)
    ```
    - ```accountReference:``` String, Required

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "contractCode": "4876165459",
            "accountReference": "Elmref6",
            "accountName": "Elmer Martin",
            "currencyCode": "NGN",
            "customerEmail": "tobi@toio.com",
            "customerName": "Mr Tobi",
            "accountNumber": "3225593799",
            "bankName": "Providus Bank",
            "bankCode": "101",
            "reservationReference": "L6KHK65ZSZJ23CKTFJKT",
            "status": "ACTIVE",
            "createdOn": "2019-11-05 12:03:16.0",
            "contract": {
            "name": "Default Contract",
            "code": "4876165459",
            "description": null,
            "supportsAdvancedSettlementAccountSelection": false
            },
            "totalAmount": 10500,
            "transactionCount": 3
        }
    }
    ```
    #### sample response - error
    ```bash
    # status 401
    {
        "error": "invalid_token",
        "error_description": "Cannot convert access token to JSON"
    }

    # status 404
    {
        "requestSuccessful": false,
        "responseMessage": "Cannot find reserved account",
        "responseCode": "99"
    }
    ```

- Delete Reserved Account
    ```python
    data = monnify.deleteReservedAccount(
        accountReference="reference_to_the_account"
    )
    print(data)
    ```
    - ```accountReference:``` String, Required

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "contractCode": "4876165459",
            "accountReference": "1576076454948",
            "accountName": "Test Payment",
            "currencyCode": "NGN",
            "customerEmail": "johndoe@email.com",
            "customerName": "John Doe",
            "accountNumber": "9749142778",
            "bankName": "Providus Bank",
            "bankCode": "101",
            "reservationReference": "HJ2YVQ63VAHETLUB94FN",
            "status": "ACTIVE",
            "createdOn": "2019-12-11 15:00:56.0"
        }
    }
    ```
    #### sample response - error
    ```bash
    # status 401
    {
        "error": "invalid_token",
        "error_description": "Cannot convert access token to JSON"
    }

    # status 404
    {
        "requestSuccessful": false,
        "responseMessage": "Cannot find reserved account",
        "responseCode": "99"
    }
    ```




- Update BVN For Reserved Account
    ```python
    data = monnify.updateBVN(
        accountReference="reference_to_the_account",
        bvn="bvn_of_account_owner"
    )
    print(data)
    ```
    - ```accountReference:``` String, Required
    - ```bvn:``` String, required

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "00",
        "responseBody": {
            "bvn": "12345678901",
            "accountReference": "ACC_REF_12345",
            "accountName": "John Doe",
            "accountNumber": "0123456789",
            "bankCode": "101",
            "bankName": "Providus Bank"
        }
    }
    ```
    #### sample response - error
    ```bash
    # status 401
    {
        "error": "invalid_token",
        "error_description": "Cannot convert access token to JSON"
    }

    # status 404
    {
        "requestSuccessful": false,
        "responseMessage": "Account not found",
        "responseCode": "99"
    }

    {
        "requestSuccessful": false,
        "responseMessage": "BVN already associated with the account",
        "responseCode": "01",
        "bvn": "12345678901",
        "accountReference": "ACC_REF_12345"
    }
    ```

### Transactions
- Initiate Transaction
    ```python
    data = monnify.initiateTransaction(
        amount=100,
        customerName="customer_full_name",
        customerEmail="customerEmail", # e.g johndoe@gmail.com
        paymentReference="unique_reference", # e.g ref1839238
        paymentDescription="paymentDescription", # description of payment
        currencyCode="NGN",
        contractCode="contractCode", # see your monnify dashboard
        redirectUrl="redirectUrl" # monnify redirect to this URL when transaction is completed
    )
    print(data)
    ```
    - ```amount:``` Number, Required
    - ```paymentReference:``` String, Required
    - ```currencyCode:``` String, Required, should be "NGN"
    - ```contractCode:``` String, Required
    - ```customerName:``` String, Required
    - ```customerEmail:``` String, Required
    - ```redirectUrl:``` String, required
    When transaction is initiated, monnify returns a checkoutUrl to make payment using monnify payment form
    ```Note:``` All transactions mst be initiated before using the bank transfer or payment with card options 

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "transactionReference": "MNFY|20191227150105|000223",
            "paymentReference": "1577458865686",
            "merchantName": "Tobi Limited",
            "apiKey": "MK_TEST_VR7J3UAACH",
            "enabledPaymentMethod": [
                "ACCOUNT_TRANSFER"
            ],
            "checkoutUrl": "https://sandbox.sdk.monnify.com/checkout/MNFY|20191227150105|000223",
            "incomeSplitConfig": []
        }
    }
    ```
    #### sample response - error
    ```bash
    # status 400
    {
        "requestSuccessful": false,
        "responseMessage": "Field contractCode cannot be null",
        "responseCode": "99"
    }

    # status 403
    {
        "requestSuccessful": false,
        "responseMessage": "Could not Authorize merchant",
        "responseCode": "99"
    }

    # status 422
    {
        "requestSuccessful": false,
        "responseMessage": "Duplicate payment reference",
        "responseCode": "99"
    }
    ```

- Pay With Bank Transfer
    usually if you don't want to use monnify's payment form using the checkoutUrl returned after initiating transaction, you can use direct APIs for bank transfer. 
     Monnify will return an account number and bank for that transaction as well as an accountDuration specifying how long the account will last (10 minutes). 
     You can also pass an optional bank code parameter and Monnify will return a USSD string for payment from that bank.
    ```python
    data = monnify.payWithBankTransfer(
        transactionReference="Transaction reference returned by Monnify when the transaction was initialized",
        bankCode="Bank Code for the bank's USSD string to be returned"
    )
    print(data)
    ```
    - ```transactionReference:``` Number, Required
    - ```bankCode:``` String, Optional

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "accountNumber": "4878539561",
            "accountName": "Is it working",
            "bankName": "Providus Bank",
            "bankCode": "101",
            "accountDurationSeconds": 165, # transaction account expiration in seconds
            "ussdPayment": "*737*2*100.00*4878539561#",
            "requestTime": "2019-12-27T15:34:13",
            "transactionReference": "MNFY|20191227150634|000260",
            "paymentReference": "1577459193045",
            "amount": 100,
            "fee": 10,
            "totalPayable": 100,
            "collectionChannel": "API_NOTIFICATION",
            "productInformation": null
        }
    }
    ```
    #### sample response - error
    ```bash
    # status 400
    {
        "requestSuccessful": false,
        "responseMessage": "Field transactionReference cannot be null",
        "responseCode": "99"
    }

    # status 403
    {
        "requestSuccessful": false,
        "responseMessage": "Could not Authorize merchant",
        "responseCode": "99"
    }

    # status 422
    {
        "requestSuccessful": false,
        "responseMessage": "could not find specified bank",
        "responseCode": "99"
    }
    ```

- Webhook Notifications
    When a transaction is processed successfully on Monnify, a webhook notification is sent to the webhook URL configured on the merchant's dashboard. merchant when a transaction has been processed successfully. 
    #### Account Transaction Notification
    This is the notification sent when an account transaction is completed using bank transfer.
    ```bash
    {
        "transactionReference":"MNFY|20190920113413|000224",
        "paymentReference":"1568979249981",
        "amountPaid":"100.00",
        "totalPayable":"100.00",
        "paidOn":"20/09/2019 11:35:21",
        "paymentStatus":"PAID",
        "paymentDescription":"Is it working",
        "transactionHash":"5a91ef93b91a0bfda95a19c18da4504506ba20f79d6c0fb9ec3907b56635e7b01360e2a9ffcb5bc1e1208df68688a6d0ce064bec968099d7466818b6826cfd66",
        "currency":"NGN",
        "paymentMethod":"ACCOUNT_TRANSFER",
        "product":{
            "type":"WEB_SDK",
            "reference":"1568979249981"
        },
        "cardDetails":null,
        "accountDetails":{
            "accountName":"OLUWATOBI EMMANUEL AMIRA",
            "accountNumber":"******7561",
            "bankCode":"000015",
            "amountPaid":"100.00"
        },
        "accountPayments":[
            {
                "accountName":"OLUWATOBI EMMANUEL AMIRA",
                "accountNumber":"******7561",
                "bankCode":"000015",
                "amountPaid":"100.00"
            }
        ],
        "customer":{
            "email":"stephen@ikhane.com",
            "name":"Stephen Ikhane"
        }
    } 
    ```
    #### Card Transaction Notification
    This is the notification sent when an account transaction is completed using a debit/credit card.
    ```bash
    {
       "transactionReference":"MNFY|20190920113413|000224",
       "paymentReference":"1568979249981",
       "amountPaid":"100.00",
       "totalPayable":"100.00",
       "paidOn":"20/09/2019 11:35:21",
       "paymentStatus":"PAID",
       "paymentDescription":"Is it working",
       "transactionHash":"5a91ef93b91a0bfda95a19c18da4504506ba20f79d6c0fb9ec3907b56635e7b01360e2a9ffcb5bc1e1208df68688a6d0ce064bec968099d7466818b6826cfd66",
       "currency":"NGN",
       "paymentMethod":"ACCOUNT_TRANSFER",
       "product":{
          "type":"WEB_SDK",
          "reference":"1568979249981"
       },
       "cardDetails":   {
          "cardType":null,
          "authorizationCode":null,
          "last4":"6871",
          "expMonth":"08",
          "expYear":"22",
          "bin":"539941",
          "reusable":false 
       },
       "accountDetails": null,
       "accountPayments": null,
       "customer":{
          "email":"stephen@ikhane.com",
          "name":"Stephen Ikhane"
       }
    }
    ```
    #### Calculating The Transaction Hash
    When Monnify sends transaction notifications, they add a transaction hash for security reasons. They expect you to try to recreate the transaction hash and only honor the notification if it matches. 
    To calculate the hash value, use the information from the notification to call the following function;
    ```python
    hash = monnify.createHashFromWebhook(
        paymentReference="paymentReference",
        amountPaid="amountPaid",
        paidOn="paidOn",
        transactionReference="transactionReference"
    )
    print(hash)
    ```
    #### sample response
    ```bash
    5a91ef93b91a0bfda95a19c18da4504506ba20f79d6c0fb9ec3907b56635e7b01360e2a9ffcb5bc1e1208df68688a6d0ce064bec968099d7466818b6826cfd66
    ```

- Settlement Notifications
    This notification is sent when a merchant is settled. It is sent to the merchant's notification endpoint configured on the settings.
    ```bash
    {
        "settlementReference": "JDFHKHDLSJD",
        "amount": 100000.00,
        "destinationAccountNumber": "0802139801",
        "destinationAccountName": "MERCHANT LIMITED",
        "destinationBankCode": "058",
        "destinationBankName": "GTBANK",
        "settlementTime": "20/09/2019 11:35:21",
        "transactionsCount": 1
    }
    ```

- Verifying Transactions/ Get Transaction Details
    On Monnify you can verify transactions using either the transactionReference automatically generated by Monnify.
    ```python
    data = monnify.getTransactionDetails(
        transactionReference="transaction_reference", # e.g ref1839238
    )
    print(data)
    ```
    - ```transactiontReference:``` String, Required

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "createdOn": "2019-09-24T08:00:59.000+0000",
            "amount": 100,
            "currencyCode": "NGN",
            "customerName": "Stephen Ikhane",
            "customerEmail": "stephen@ikhane.com",
            "paymentDescription": "Test push payment config",
            "paymentStatus": "PENDING",
            "transactionReference": "MNFY|20190924080058|000004",
            "paymentReference": "1569312056285"
        }
    }
    ```
    #### sample response - error
    ```bash
    # status 403
    {
        "requestSuccessful": false,
        "responseMessage": "Could not Authorize merchant",
        "responseCode": "99"
    }

    # status 404
    {
        "requestSuccessful": false,
        "responseMessage": "Could not find transaction with the specified transaction reference",
        "responseCode": "99"
    }
    ```


### Sub Accounts / Split Settlements
With sub accounts, you can easily split a single payment across multiple accounts. This means for one transaction, Monnify can help you share the amount paid between up to 5 different accounts. 
To use split payments, you need to create sub accounts. Sub accounts can be created and managed on the Monnify Dashboard or via APIs.
- Create A Sub Account
    ```python
    data = monnify.createSubAccount(
        bankCode="101", # bank code of sub account
        accountNumber="0123456789", # account numer of sub account
        email="accounts@monnify.com", # email of user account
        splitPercentage="20" # percentage of payment to be received in this account
    )
    print(data)
    ```
    - ```bankCode:``` String, Required
    - ```accountNumber:``` String, Required
    - ```email:``` String, Required
    - ```splitPercentage:``` String, Required

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": [
            {
            "subAccountCode": "MFY_SUB_319452883328",
            "accountNumber": "0123456789",
            "accountName": "Customers Logistics Subaccount",
            "currencyCode": "NGN",
            "email": "accounts@monnify.com",
            "bankCode": "101",
            "bankName": "Providus",
            "defaultSplitPercentage": 20
            }
        ]
    }
    ```

- Get All Sub Accounts
    ```python
    data = monnify.getSubAccounts()
    print(data)
    ```
     #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": [
            {
            "subAccountCode": "MFY_SUB_319452883328",
            "accountNumber": "0123456789",
            "accountName": "Customers Logistics Subaccount",
            "currencyCode": "NGN",
            "email": "accounts@monnify.com",
            "bankCode": "101",
            "bankName": "Providus",
            "defaultSplitPercentage": 20
            },
            {
            "subAccountCode": "MFY_SUB_8838656722391",
            "accountNumber": "9876543210",
            "accountName": "JANE, DOE SNOW",
            "currencyCode": "NGN",
            "email": "tamira2@gmail.com",
            "bankCode": "057",
            "bankName": "Zenith bank",
            "defaultSplitPercentage": 50
            }
        ]
    }
    ```

- Update A Sub Account
    ```python
    data = monnify.updateSubAccount(
        subAccountCode="MFY_SUB_319452883328", # sub account code of the sub account to update
        bankCode="058",
        accountNumber="0123456789",
        email="tamira3@gmail.com",
        splitPercentage="25"
    )
    print(data)
    ```
     #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": [
            {
            "subAccountCode": "MFY_SUB_319452883328",
            "accountNumber": "0123456789",
            "accountName": "JOHN, DOE SNOW",
            "currencyCode": "NGN",
            "email": "tamira1@gmail.com",
            "bankCode": "058",
            "bankName": "GTBank",
            "defaultSplitPercentage": 20
            }
        ]
    }
    ```

- Delete A Sub Account
    ```python
    data = monnify.deleteSubAccount(
        subAccountCode="MFY_SUB_319452883328", # sub account code of the sub account to delete
    )
    print(data)
    ```
     #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0"
    }
    ```

### Disbursement Transactions / Transfers
The Monnify Disbursements APIs allow a merchant to initiate payouts from his Monnify Wallet to any bank account in Nigeria. They provide all the tools you need to enable you completely automate your disbursement processes.
- Initiate A Single Transfer
    To initiate a single transfer, you will need to send a request to the endpoint. If the merchant does not have Two Factor Authentication (2FA) enabled, the transaction will be processed instantly as in the response. If 2FA is enabled, the response will indicate stutus as pending authorization.
    ```python
    data = monnify.initiateSingleTransfer(
        amount=100,
        reference="reference12934",
        narration="911 Transaction",
        bankCode="058",
        accountNumber="0111946768",
        walletId="4794983C91374AD6B3ECD76F2BEA296D"
    )
    print(data)
    ```
    - ```amount:``` Number, required; The amount to be disbursed to the beneficiary
    - ```reference:``` String, required; The unique reference for a transaction. Also to be specified for each transaction in a bulk transaction request.
    - ```narration:``` String, required; The Narration for the transactions being processed.
    - ```bankCode:``` String, Required; The 3 digit bank code representing the destination bank.
    - ```accountNumber:``` String, Required; The beneficiary account number.
    - ```walletId:``` String, Required; Unique reference to identify the wallet to be debited.

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "amount": 10,
            "reference": "reference12934",
            "status": "SUCCESS",
            "dateCreated": "13/11/2019 09:34:32 PM"
        }
    }
    # Pending Authorization
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "amount": 10,
            "reference": "reference12934",
            "status": "PENDING_AUTHORIZATION",
            "dateCreated": "13/11/2019 08:48:32 PM"
        }
    }
    ```

- Initiate A Bulk Transfer
    To initiate a bulk transfer, you will need to send a request to the endpoint. If the merchant does not have Two Factor Authentication (2FA) enabled, the transaction will be processed instantly as in the response. If 2FA is enabled, the response will indicate stutus as pending authorization. 
    When a bulk transfer request is sent, it is simply acknowledged by the system and then processed in the background. Monnify goes through each account to attempt to validate them and depending on what value is set for the onValidationFailure field, Monnify will either continue processing with the valid transfers or reject the entire batch. 
    Use ```BREAK``` to tell Monnify to reject the entire batch and use ```CONTINUE``` to tell Monnify to process the valid transactions.
    ```python
    # define the lists of transactions to be performed
    transaction_list = [
        {
            "amount": 1300,
            "reference": "Final-Reference-1a",
            "narration": "911 Transaction",
            "bankCode": "058",
            "accountNumber": "0111946768",
            "currency": "NGN"
        },
        {
            "amount": 570,
            "reference": "Final-Reference-2a",
            "narration": "911 Transaction",
            "bankCode": "058",
            "accountNumber": "0111946768",
            "currency": "NGN"
        },
        {
            "amount": 230,
            "reference": "Final-Reference-3a",
            "narration": "911 Transaction",
            "bankCode": "058",
            "accountNumber": "0111946768",
            "currency": "NGN"
        }
    ]
    # make the request
    data = monnify.initiateBulkTransfer(
        title="title of the transfer",
        batchReference="unique reference for batch",
        narration="narration of the bulk transfer",
        walletId="4794983C91374AD6B3ECD76F2BEA296D", #Unique reference to identify the wallet to be debited.
        onValidationFailure="CONTINUE",
        transactionList=transaction_list
    )
    print(data)
    ```
    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "totalAmount": 2108.48,
            "totalFee": 8.48,
            "batchReference": "batch-1573681308355",
            "batchStatus": "COMPLETED",
            "totalTransactions": 3,
            "dateCreated": "13/11/2019 09:42:06 PM"
        }
    }
    # Pending Authorization
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "totalAmount": 2108.48,
            "totalFee": 8.48,
            "batchReference": "batch-1573684027157",
            "batchStatus": "PENDING_AUTHORIZATION",
            "totalTransactions": 3,
            "dateCreated": "13/11/2019 10:27:25 PM"
        }
    }
    ```

- Authorize A Single Transfer
    To authorize a single transfer for 2FA, you will need to send the following request
    ```python
    data = monnify.authorizeSingleTransfer(
        reference="reference12934",
        authorizationCode="40538652"
    )
    print(data)
    ```
    - ```reference:``` String, required; The unique reference for a transaction.
    - ```authorizationCode:``` String, required; The One Time Password sent to the specified email to be used to authenticate the transaction.

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "amount": 10,
            "reference": "reference12934",
            "status": "SUCCESS",
            "dateCreated": "13/11/2019 09:34:32 PM"
        }
    }
    ```

- Authorize Bulk Transfer
    To authorize a bulk transfer for 2FA, you will need to send the following request
    ```python
    data = monnify.authorizeBulkTransfer(
        reference="batch-reference12934",
        authorizationCode="40538652"
    )
    print(data)
    ```
    - ```reference:``` String, required; The unique reference for batch transaction Also to be specified for each transaction in a bulk transaction request
    - ```authorizationCode:``` String, required; The One Time Password sent to the specified email to be used to authenticate the transaction.

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "amount": 10,
            "reference": "batch-reference12934",
            "status": "SUCCESS",
            "dateCreated": "13/11/2019 09:34:32 PM"
        }
    }
    ```

- Resend OTP
    To resend OTP for 2FA, you will need to send the following request.
    ```python
    data = monnify.resendOTP(
        reference="reference"
    )
    print(data)
    ```
    - ```reference:``` String, required; The unique reference for batch transaction Also to be specified for each transaction in a bulk transaction request

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "message": "Authorization code will be processed and sent to predefined email addresses(s)"
        }
    }
    ```

- Get Single Transfer Status
    ```python
    data = monnify.getSingleTransferStatus(
        reference="reference"
    )
    print(data)
    ```
    - ```reference:``` String, required; The unique reference for single transaction

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "amount": 230,
            "reference": "Final-Reference-3a",
            "narration": "911 Transaction",
            "bankCode": "058",
            "accountNumber": "0111946768",
            "currency": "NGN",
            "accountName": "MEKILIUWA, SMART CHINONSO",
            "bankName": "GTBank",
            "dateCreated": "13/11/2019 09:42:07 PM",
            "fee": 1,
            "status": "SUCCESS"
        }
    }
    ```

- Get Bulk Transfer Status
    ```python
    data = monnify.getBulkTransferStatus(
        reference="reference"
    )
    print(data)
    ```
    - ```reference:``` String, required; The unique reference for bulk transaction

    #### sample response - success
    ```bash
    # status 200
    {
        "requestSuccessful": true,
        "responseMessage": "success",
        "responseCode": "0",
        "responseBody": {
            "title": "Final Batch - Continue on Failure",
            "totalAmount": 2108.48,
            "totalFee": 8.48,
            "batchReference": "batchreference12934",
            "totalTransactions": 3,
            "failedCount": 0,
            "successfulCount": 0,
            "pendingCount": 3,
            "batchStatus": "AWAITING_PROCESSING",
            "dateCreated": "13/11/2019 10:45:08 PM"
        }
    }
    ```
