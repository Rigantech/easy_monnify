import requests
import json
from base64 import b64encode
import hashlib

"""
{
                    "subAccountCode": kwargs["subAccountCode"],
                    "splitAmount": kwargs["splitAmount"],
                    "feePercentage": kwargs["feePercentage"],
                    "feabearer": kwargs["feeBearer"],
                    "splitPercentage": kwargs["splitPercentage"]
                }
"""

base_url = {
    "sandbox": "https://sandbox.monnify.com",
    "live": "https://api.monnify.com"
}

class Monnify:
    def __init__(self, apiKey, clientSecretKey, environment="live"):
        self.apiKey = apiKey
        self.clientSecretKey = clientSecretKey
        self.base_url = base_url[environment]

    """ Generates Token"""
    def generateToken(self):
        data = f"{self.apiKey}:{self.clientSecretKey}".encode()
        userAndPass = b64encode(data).decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  userAndPass }
        #print(headers)
        url = f"{self.base_url}/api/v1/auth/login"
        r = requests.post(url, headers=headers)
        loadJson = json.loads(r.content)
        #print(loadJson['responseBody']['accessToken'])
        token = loadJson['responseBody']['accessToken']
        return token


    #======================= Reserved Accounts ==================================
    """ Create Reserve Account v1"""
    def createReservedAccount(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        reserveAccUrl = f"{self.base_url}/api/v1/bank-transfer/reserved-accounts"
        data = {
            "accountReference":kwargs["accountReference"],
            "accountName":kwargs["accountName"],
            "currencyCode":"NGN",
            "contractCode":kwargs["contractCode"],
            "customerEmail":kwargs["customerEmail"],
            "customerName":kwargs["customerName"],
            "reservedAccountType": "INVOICE"
            }
        createReserveAccount = requests.post(reserveAccUrl, data=json.dumps(data), headers=rHeaders)
        reserverR = json.loads(createReserveAccount.content)
        #print("==>", reserverR)
        return reserverR

    # get Reserved account details
    def getReservedAccountDetails(self, accountReference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f"{self.base_url}/api/v1/bank-transfer/reserved-accounts/"+accountReference
        getAccDetails = requests.get(url, headers=rHeaders)
        accDetails = json.loads(getAccDetails.content)
        return accDetails

    # delete reserved account
    def deleteReservedAccount(self, accountReference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f"{self.base_url}/api/v1/bank-transfer/reserved-accounts/"+accountReference
        delete_account = requests.delete(url, headers=rHeaders)
        acc_details = json.loads(delete_account.content)
        return acc_details

    # add linked accounts, not added
    def addLinkedAccounts(self, accountReference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/bank-transfer/reserved-accounts/add-linked-accounts/'+accountReference
        data = {
            "getAllAvailableBanks": True,
        }
        addAccount = requests.post(url, data=json.dumps(data), headers=rHeaders)
        accDetails = json.loads(addAccount.content)
        return accDetails

    # update bvn for reserved account
    def updateBVN(self, accountReference, bvn):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/bank-transfer/reserved-accounts/update-customer-bvn/'+accountReference
        data = {
            "bvn": bvn,
        }
        update_bvn = requests.post(url, data=json.dumps(data), headers=rHeaders)
        bvn_details = json.loads(update_bvn.content)
        return bvn_details

        

    #============================ Transactions =====================================

    # Initiate a transaction
    def initiateTransaction(self,**kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/merchant/transactions/init-transaction'
        data = {
            "amount": kwargs["amount"],
            "customerName": kwargs["customerName"],
            "customerEmail": kwargs["customerEmail"],
            "paymentReference": kwargs["paymentReference"],
            "paymentDescription": kwargs["paymentDescription"],
            "currencyCode": "NGN",
            "contractCode": kwargs["contractCode"],
            "redirectUrl": kwargs["redirectUrl"],
            "incomeSplitConfig": []
        }
        initTransaction = requests.post(url, data=json.dumps(data), headers=rHeaders)
        transaction = json.loads(initTransaction.content)
        #print("==>", reserverR)
        return transaction

    # pay with Bank Transfer
    def payWithBankTransfer(self, transactionReference, bankCode):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/merchant/bank-transfer/init-payment'
        data = {
            "transactionReference": transactionReference,
            "bankCode": bankCode
        }
        initTransaction = requests.post(url, data=json.dumps(data), headers=rHeaders)
        transaction = json.loads(initTransaction.content)
        #print("==>", reserverR)
        return transaction

    
    # charge card payment, not added
    def payWithCard(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/merchant/cards/charge'
        data = {
            "transactionReference": kwargs["transactionReference"],
            "collectionChannel": "API_NOTIFICATION",
            "card": {
                "number": kwargs["cardNumber"],
                "pin": kwargs["cardPin"],
                "expiryMonth": kwargs["expiryMonth"],
                "expiryYear": kwargs["expiryYear"],
                "cvv": kwargs["cvv"]
            }
        }
        chargeCard = requests.post(url, data=json.dumps(data), headers=rHeaders)
        otpResponse = json.loads(chargeCard.content)
        #print("==>", reserverR)
        return otpResponse


    # authorize OTP, not added
    def authorizeOTP(self, transactionReference, tokenId, token):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/merchant/cards/charge'
        data = {
            "transactionReference": transactionReference,
            "collectionChannel": "API_NOTIFICATION",
            "tokenId": tokenId,
            "token": token
        }
        authorize_otp = requests.post(url, data=json.dumps(data), headers=rHeaders)
        otpResponse = json.loads(authorize_otp.content)
        #print("==>", reserverR)
        return otpResponse
    

    # get reserved account transactions, not added
    def getAccountTransactions(self, accountReference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/bank-transfer/reserved-accounts/transactions?accountReference={accountReference}&page=0&size=10'
        getTrans = requests.get(url, headers=rHeaders)
        transObj = json.loads(getTrans.content)
        return transObj


    # Get all transactions, not added
    def getAllTransactions(self, params):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/transactions/search?'+params
        getTrans = requests.get(url, headers=rHeaders)
        transObj = json.loads(getTrans.content)
        return transObj


    """GET TRANSACTION DETAILS"""
    def getTransactionDetails(self,transactionReference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/merchant/transactions/query?transactionReference='+transactionReference
        getTrans = requests.get(url, headers=rHeaders)
        details = json.loads(getTrans.content)
        return details


    #========================= Sub Accounts ========================================

    # create subaccount
    def createSubAccount(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/sub-accounts'
        data = [
            {
                "currencyCode": "NGN",
                "bankCode": kwargs["bankCode"],
                "accountNumber": kwargs["accountNumber"],
                "email": kwargs["email"],
                "defaultSplitPercentage": kwargs["splitPercentage"]
            }
        ]
        create_acc = requests.post(url, data=json.dumps(data), headers=rHeaders)
        acc_details = json.loads(create_acc.content)
        return acc_details


    # delete subaccount
    def deleteSubAccount(self, subAccountCode):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/sub-accounts/?subAccountCode='+subAccountCode
        delete_acc = requests.delete(url, headers=rHeaders)
        acc_details = json.loads(delete_acc.content)
        return acc_details


    # get subaccounts
    def getSubAccounts(self):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/sub-accounts/'
        get_accounts = requests.get(url, headers=rHeaders)
        accounts = json.loads(get_accounts.content)
        return accounts


    # update subaccounts
    def updateSubAccount(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/sub-accounts'
        data = [
            {
                "subAccountCode": kwargs["subAccountCode"],
                "currencyCode": "NGN",
                "bankCode": kwargs["bankCode"],
                "accountNumber": kwargs["accountNumber"],
                "email": kwargs["email"],
                "defaultSplitPercentage": kwargs["splitPercentage"]
            }
        ]
        create_acc = requests.put(url, data=json.dumps(data), headers=rHeaders)
        acc_details = json.loads(create_acc.content)
        return acc_details


    # update split config for reserved accounts, not added
    def updateSplitConfig(self, accountReference, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/bank-transfer/reserved-accounts/update-income-split-config/'+accountReference
        data = {
            "subAccountCode": kwargs["subAccountCode"],
            "feebearer": True,
            "feePercentage": kwargs["feePercentage"],
            "splitPercentage": kwargs["splitPercentage"],
        }
        update_split = requests.post(url, data=json.dumps(data), headers=rHeaders)
        split_details = json.loads(update_split.content)
        return split_details
        
        
    #================================= Transfers ==========================================

    # initiate single transfer
    def initiateSingleTransfer(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/single'
        data = {
            "amount": int(kwargs["amount"]),
            "reference": kwargs["reference"],
            "narration": kwargs["narration"],
            "bankCode": kwargs["bankCode"],
            "accountNumber": kwargs["accountNumber"],
            "currency": "NGN",
            "walletId": kwargs["walletId"]
        }
        initiate_transfer = requests.post(url, data=json.dumps(data), headers=rHeaders)
        transfer = json.loads(initiate_transfer.content)
        return transfer
    
    # initiate bulk transfer
    def initiateBulkTransfer(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/batch'
        data = {
            "title": kwargs["title"],
            "batchReference": kwargs["batchReference"],
            "narration": kwargs["narration"],
            "onValidationFailure": kwargs["onValidationFailure"],
            "notificationInterval": 10,
            "walletId": kwargs["walletId"],
            "transactionList": kwargs["transactionList"]
        }
        initiate_transfer = requests.post(url, data=json.dumps(data), headers=rHeaders)
        transfer = json.loads(initiate_transfer.content)
        return transfer


    # authorize single transfer
    def authorizeSingleTransfer(self, reference, authorizationCode):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/single/validate-otp'
        data = {
            "reference": reference,
            "authorizationCode": authorizationCode
        }
        authorize_transfer = requests.post(url, data=json.dumps(data), headers=rHeaders)
        transfer = json.loads(authorize_transfer.content)
        return transfer
    
    # authorize bulk transfer
    def authorizeBulkTransfer(self, reference, authorizationCode):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/batch/validate-otp'
        data = {
            "reference": reference,
            "authorizationCode": authorizationCode
        }
        authorize_transfer = requests.post(url, data=json.dumps(data), headers=rHeaders)
        transfer = json.loads(authorize_transfer.content)
        return transfer
    
    # resend OTP
    def resendOTP(self, reference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/single/resend-otp'
        data = {
            "reference": reference,
        }
        resend_otp = requests.post(url, data=json.dumps(data), headers=rHeaders)
        transfer = json.loads(resend_otp.content)
        return transfer


    # transfer status
    def getSingleTransferStatus(self, reference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/single/summary?reference=?reference='+reference
        transfer_status = requests.get(url, headers=rHeaders)
        transfer = json.loads(transfer_status.content)
        return transfer
    
    # transfer status
    def getBulkTransferStatus(self, reference):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/batch/summary?reference=?reference='+reference
        transfer_status = requests.get(url, headers=rHeaders)
        transfer = json.loads(transfer_status.content)
        return transfer


    # transfer status
    def searchTransfers(self, params):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v2/disbursements/search-transactions?'+params
        search_transfers = requests.get(url, headers=rHeaders)
        transfers = json.loads(search_transfers.content)
        return transfers


    # get all transfers
    def getAllTransfers(self, pageSize, pageNumber):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v2/disbursements/single/transactions?pageSize={pageSize}&pageNo={pageNumber}'
        get_transfers = requests.get(url, headers=rHeaders)
        transfers = json.loads(get_transfers.content)
        return transfers


    #=========================== Wallet =======================================#

    # Get Wallet Balance
    def getWalletBalance(self, accountNumber):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v2/disbursements/wallet-balance?accountNumber='+accountNumber
        get_balance = requests.get(url, headers=rHeaders)
        balance = json.loads(get_balance.content)
        return balance

    
    # Get available banks
    def getBanks(self):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/banks'
        get_banks = requests.get(url, headers=rHeaders)
        banks = json.loads(get_banks.content)
        return banks


    # Get available banks USSD
    def getBanksUSSD(self):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/sdk/transactions/banks'
        get_banks_ussd = requests.get(url, headers=rHeaders)
        banks_ussd = json.loads(get_banks_ussd.content)
        return banks_ussd

    
    # ======================= Bank Verification ============================================

    #verify account
    def verifyAccount(self, accountNumber, bankCode):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/disbursements/account/validate?accountNumber={accountNumber}&bankCode={bankCode}'
        verify_account = requests.get(url, headers=rHeaders)
        account = json.loads(verify_account.content)
        return account


    # verify bvn number
    def verifyBvn(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/vas/bvn-details-match'
        data = {
            "bvn": kwargs["bvn"],
            "name": kwargs["name"],
            "dateOfBirth": kwargs["dateOfBirth"],
            "mobileNo": kwargs["mobileNo"]
        }
        verify_bvn = requests.post(url, data=json.dumps(data), headers=rHeaders)
        account = json.loads(verify_bvn.content)
        return account


    # verify bvn account
    def verifyBvnDetails(self, **kwargs):
        rHeaders = {'Content-Type':"application/json", 'Authorization':"Bearer {0}".format(self.generateToken())}
        url = f'{self.base_url}/api/v1/vas/bvn-account-match'
        data = {
            "bvn": kwargs["bvn"],
            "bankCode": kwargs["bankCode"],
            "accountNumber": kwargs["accountNumber"]
        }
        verify_bvn = requests.post(url, data=json.dumps(data), headers=rHeaders)
        account = json.loads(verify_bvn.content)
        return account


    """ Check verify valid payment"""
    def createHashFromWebhook(self, paymentReference, amountPaid, paidOn, transactionReference):
        to_hash = f'{self.clientSecretKey}|{paymentReference}|{amountPaid}|{paidOn}|{transactionReference}'
        hash_value = hashlib.sha512(to_hash.encode()).hexdigest()
        return hash_value

 