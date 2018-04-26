ICON SDK for python
========

 ICON supports SDK for 3rd party or user services development.  You can integrate ICON SDK for your project and utilize ICON’s functionality.

 - [Prerequisite](#prerequisite)
 - [Version](#version)
 - [Glossary](#glossary)
 - [Technical information](#technical-information)
 - [Modules](#modules)
 - [Getting started](#getting-started)
 	- [Example](#example)
 - [Functions of wallet](#functions-of-wallet)
 	- [create_keystore_file_of_wallet(keystore_file_path, password)](#createkeystorefileofwallet)
 		- [Arguments](#arguments)
 		- [Successful case](#successful-case)
 		- [Error cases](#error-cases)
 	- [create_wallet_by_private_key(hex_private_key)](#createwalletbyprivatekeyhexprivatekey)
 		- [Arguments](#arguments)
 		- [Successful case](#successful-case)
 		- [Error cases](#error-cases)
 	- [open_keystore_file_of_wallet(keystore_file_path, password)](#openkeystorefileofwalletkeystorefilepath-password)
 		- [Arguments](#arguments)
 		- [Successful case](#successful-case)
 		- [Error cases](#error-cases)
 	- [transfer_value(password, to_address, value, fee=10000000000000000, uri, hex_private_key=None, **kwargs)](#transfervaluepassword-toaddress-value-fee10000000000000000-uri-hexprivatekeynone-kwargs)
 		- [Arguments](#arguments)
 		- [TIP](#tip)
 		- [Successful case](#successful-case)
 		- [Unsuccessful case](#unsuccessful-case)
 		- [Error cases](#error-cases)
 	- [get_wallet_info(uri)](#getwalletinfouri)
 		- [Arguments](#arguments)
 		- [Successful case](#successful-case)
 		- [Error cases](#error-cases)
 	- [get_balance(uri)](#getbalanceuri)
 		- [Arguments](#arguments)
 		- [Successful case](#successful-case)
 		- [Error cases](#error-cases)
 	- [get_address()](#getaddress)
 		- [Arguments](#arguments)
 		- [Successful case](#successful-case)
 		- [Error cases](#error-cases)

# Prerequisite

* Python 3.6.x

# Version

* 0.0.1 beta

# Glossary

* Address of wallet : Unique string to identify the address to transfer value. It begins with hx.

* Private key: A tiny bit of code that is paired with a public key to set off algorithms to encrypt and decrypt a text  for the specific address.

* Public key: Long alphanumeric characters that is used to encrypt data (message).

# Technical information

There are five steps to get from  private->public -> address:

1. Generate a private key.

2. Derive a public key from the private key.

3. H1 = sha3_256( Public key)  => 32 byte

4. BitAddress = last 20 bytes of H1

5. Address = hx || HexString(BitAddress)
ex) hxaa688d74eb5f98b577883ca203535d2aa4f0838c

# Modules

* ```wallet``` : Package name of ICX wallet functions.

# Getting started

```shell
$ pip install icxapi
```

## Example
```python

from icx.wallet.wallet import Wallet

# Create a keystore file of a wallet.
my_wallet_1, _ = Wallet.create_keystore_file_of_wallet(keystore_file_path="./keystore.txt", password="test1234*")

# Create a wallet by the private key.
my_wallet_2, _ = Wallet.create_wallet_by_private_key(hex_private_key="")

# Open the keystore file of the wallet.
my_wallet_3, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path="./test_keystore_for_transfer.txt", password="ejfnvm1234*")

# Get balance.
balance = my_wallet_1.get_balance(uri="https://testwallet.icon.foundation/api/")

# Get information of the wallet.
wallet_info = my_wallet_1.get_wallet_info(uri="https://testwallet.icon.foundation/api/")

# Get an address.
wallet_address = my_wallet_1.get_address()

# Transfer value 1,010,000,000,000,000,000 loop (1.01 icx) with 10,000,000,000,000,000 loop (0.01 icx) fee.
try:
    result = my_wallet_3.transfer_value(password="ejfnvm1234*", to_address="hx68bc6f60ea01bc033504a217631c601386be26b7", \
                value="1010000000000000000", fee=10000000000000000)
except PasswordIsNotAcceptable:
    print(f"Password is not acceptable.")
except PasswordIsWrong:
     print(f"Password is wrong.")
except AddressIsWrong:
     print(f"Wallet address is wrong.")
except NotEnoughBalanceInWallet:
     print(f"Balance is not enough.")
except TransferFeeIsInvalid:
     print(f"Transaction Fee is invalid. The fee should be 10000000000000000.")
except FeeIsBiggerThanAmount:
     print(f"Fee is bigger than transaction amount.")
except AmountIsInvalid:
     print(f"The amount you want to transfer is not valid.")
except AddressIsSame:
     print(f"Wallet address to transfer must be different from Wallet address to deposit.")

```

# Functions of wallet

## ```create_keystore_file_of_wallet(keystore_file_path, password)```

create both a wallet and a keystore file with file path and given password.

### Arguments

* ```keystore_file_path``` : File path for the keystore file of the wallet.

* ```password```: Password for the wallet. Password must include alphabet character, number, and  special character.

### Successful case

* Return : Instance of Wallet, private key

### Error cases

It will raise following exception.

* ```PasswordIsNotAcceptable```: Password is not acceptable. It must be more than eight characters long, contain any letters from **a** to **z**, any numbers from **0** to **9** and some special characters, including @ (at sign), .(period), -(hyphen or dash), and(or) _ (underscore).

* ```FilePathIsWrong```: File path is wrong.

## ```create_wallet_by_private_key(hex_private_key)```

create wallet without keystore file.

### Arguments

* ```hex_private_key``` : A private key in hexadecimal - 256 bits in hexadecimal is 32 bytes, or 64 characters in the range 0-9 or A-F. A tiny bit of code that is paired with a public key to set off algorithms to encrypt and decrypt a text for the specific address.

### Successful case

* Return : Instance of Wallet, private key

### Error cases

It will raise following exception.

* ```TypeError```

## ```open_keystore_file_of_wallet(keystore_file_path, password)```

Open the created keystore file and read the information of the file.

### Arguments

* ```keystore_file_path``` : File path for the keystore file of the wallet.

* ```password```: Password for the wallet. Password must include alphabet character, number, and  special character.

### Successful case

* Return :  Instance of Wallet.

### Error cases

It will raise following exception.

* ```PasswordIsWrong```: Password is wrong.

* ```FilePathIsWrong```: File path is wrong.

## ```transfer_value(password, to_address, value, fee=10000000000000000, uri, hex_private_key=None, **kwargs)```

Transfer the value from the given wallet to the specific address with the fee.

### Arguments

* ```password``` : Password for the wallet in keystore file used in open_wallet_from_file()

* ```to_address```: Address of the wallet

* ```value``` : Amount of money

* ```fee``` : Transfer fee (10000000000000000 loop)

* ```uri``` : URI of ICON API. The default value is 'https://testwallet.icon.foundation/api/', test net. You can use another URI of ICON API for various test net like Ethereum.

* ```kwargs``` : (Optional) Reserved for the next version

### TIP

* value and fee are integer with decimal point 10^18. Ex) 1.10 icx => 1.10 X 1,000,000,000,000,000,000 = 1,100,000,000,000,000,000 loop.

### Successful case

* Return : Response

``` json
{
    "jsonrpc": "2.0",
    "result": {
        "response_code": 0,
        "tx_hash": "4bf74e6aeeb43bde5dc8d5b62537a33ac8eb7605ebbdb51b015c1881b45b3aed"
    },
    "id":2
}
```
* ```response_code```: JSON RPC error code.
* ```tx_hash```: Hash data of the result. Use icx_getTransactionResult to get the result.
* ```id```: It MUST be the same as the value of the id member in the Request Object.

    * If there was an error in detecting the id in the Request object (e.g. Parse error/Invalid Request), it MUST be Null.

### Unsuccessful case

* Return : Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "message": "create tx message",
        "response_code": -11
    },
    "id": 2
}
```

### Error cases

It will raise following exception.

* ```AddressIsWrong``` : Wallet address is wrong.

* ```PasswordIsWrong```: Password is wrong.

* ```NoEnoughBalanceInWallet``` : Sender’s wallet does not have enough balance.

* ```TransferFeeIsInvalid``` :  Transfer fee is invalid.

* ```TimestampIsNotCorrect``` : Timestamp is not correct. (Adjust your computer’s time and date.)


## ```get_wallet_info(uri)```

Get the keystore file information and the balance.

### Arguments

* ```uri``` : URI of ICON API. The default value is 'https://testwallet.icon.foundation/api/', test net. You can use another URI of ICON API for various test net like Ethereum.

### Successful case

Return dictionary with sub items like below.

* ```balance``` : the balance of this wallet

* ```depositAddress```: the address of this wallet

* ```completedTransactions``` : list of dictionary to store completed transactions

    * ```requestedTime``` : The time when the transaction was requested

    * ```transactionType``` : deposit or withdraw

    * ```transactionID``` : ID of transaction to track

    * ```amount``` : The amount of money

* ```pendingTransactions``` :  list of dictionary to store pending transactions

    * ```requestedTime``` : The time when the transaction was requested

    * ```transactionType``` : deposit or withdraw

    * ```transactionID``` : ID of transaction to track

    * ```amount``` :  The amount of money

### Error cases

It will raise following exception.

* ```AddressIsWrong``` : Address is wrong.

## ```get_balance(uri)```

Get the balance of all addresses in the current wallet.

### Arguments

* ```uri``` : URI of ICON API. The default value is 'https://testwallet.icon.foundation/api/', test net. You can use another URI of ICON API for various test net like Ethereum.

### Successful case

* Return integer with decimal point 10^18.
Ex) 1.10 icx => It will return 1,100,000,000,000,000,000.

### Error cases

It will raise following exception.

* ```AddressIsWrong``` : Address is wrong.

## ```get_address()```

Get the address of wallet.

### Arguments

* N/A

### Successful case

* Return string of wallet address begins from ‘hx’.

### Error cases

It will raise following exception.

* ```AddressIsWrong``` : Address is wrong.
