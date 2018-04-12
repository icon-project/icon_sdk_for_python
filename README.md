ICON SDK for python
========

 ICON supports SDK for 3rd party or user services development.  You can integrate ICON SDK for your project and utilize ICON’s functionality.

<!-- TOC depthFrom:1 depthTo:4 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Prerequisite](#prerequisite)
- [Version](#version)
- [Glossary](#glossary)
- [Technical information](#technical-information)
- [Modules](#modules)
- [Getting started](#getting-started)
	- [Example](#example)
- [Functions of wallet](#functions-of-wallet)
	- [```create(password, file_path)```](#createpassword-filepath)
	- [```open_wallet_from_file (password, file_path)```](#openwalletfromfile-password-filepath)
	- [```transfer_value(wallet_info, to_address, value, password, fee=0, **kwargs )```](#transfervaluewalletinfo-toaddress-value-password-fee0-kwargs-)
- [Functions of ```WalletInfo```](#functions-of-walletinfo)
	- [```get_address_info()```](#getaddressinfo)
	- [```get_balance()```](#getbalance)
	- [```get_address()```](#getaddress)

<!-- /TOC -->

# Prerequisite

* Python 3.6.x

# Version

* 0.01 beta

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

* ```wallet``` : Capsulized functions of wallet

* ```wallet.WalletInfo``` : Class to represent the information of wallet

# Getting started

```shell
$ pip install icxapi
```

## Example
```python
from icx import wallet

# Create wallet.
my_wallet_info = wallet.create(password = "as1v1$@1", file_path = “./key_folder/key.store” )


# Get balance.
balance = my_wallet_info.get_balance()


# Transfer value 1.1 icx with 0.01 icx fee.
try:
    result = wallet.transfer_value(
        wallet_info = my_wallet_info,
        password = “as1v1$@1”
        to_address = ”hx2d76757c482857a099de21a9821ea973379f683d”,\
        value = 1100000000000000000,\
        fee   =   10000000000000000 \
        )
except AddressIsWrong:
     print(f”Wallet address is wrong.”)
except PasswordIsWrong:
     print(f”Wallet password is wrong.”)
except NotEnoughBalanceInWallet:
     print(f”Balance is not enough.”)
except TransferFeeIsInvalid:
     print(f”Transfer fee is invalid.”)
except TimestampIsNotCorrect:
     print(f”Timestamp is not correct.”)

```


# Functions of wallet

## ```create(password, file_path)```

Create a wallet file with given password and file path.

### Arguments

* ```password```: Password for the wallet. Password must include alphabet character, number, and  special character.

* ```file_path``` : File path for the keystore file of the wallet.

### Successful case

* Return : Instance of WalletInfo

### Error cases

It will raise following exception.

* ```PasswordIsNotAcceptable```: Password is not acceptable. It must be more than eight characters long, contain any letters from **a** to **z**, any numbers from **0** to **9** and some special characters, including @ (at sign), .(period), -(hyphen or dash), and(or) _ (underscore).

* ```FilePathIsWrong```: File path is wrong.

## ```open_wallet_from_file (password, file_path)```

Open the created wallet file.

### Arguments

* ```password``` : Password for the wallet in keystore file from file_path.

* ```file_path``` : File path for the keystore file of the wallet.

### Successful case

* Return :  Instance of WalletInfo.

### Error cases

It will raise following exception.

* ```PasswordIsWrong```: Password is wrong.

* ```FilePathIsWrong```: File path is wrong.

## ```transfer_value(wallet_info, to_address, value, password, fee=0, **kwargs )```

Transfer the value from the given wallet to the specific address with the fee.

### Arguments

* ```wallet_info``` : Instance of wallet class

* ```to_address```: Address of the wallet

* ```value``` : Amount of money

* ```password``` : Password for the wallet in keystore file used in open_wallet_from_file()

* ```fee``` : Transfer fee

* ```kwargs``` : (Optional) Reserved for the next version

### TIP

* value and fee are integer with decimal point 10^18. Ex) 1.10 icx => 1.10 X 1,000,000,000,000,000,000 = 1,100,000,000,000,000,000.


### Successful case

Return 0 : Succeed to transfer

### Error cases

It will raise following exception.

* ```AddressIsWrong``` : Wallet address is wrong.

* ```PasswordIsWrong```: Password is wrong.

* ```NoEnoughBalanceInWallet``` : Sender’s wallet does not have enough balance.

* ```TransferFeeIsInvalid``` :  Transfer fee is invalid.

* ```TimestampIsNotCorrect``` : Timestamp is not correct. (Adjust your computer’s time and date.)

# Functions of ```WalletInfo```

## ```get_address_info()```

Get the information of address.

### Arguments

* N/A

### Successful case

Return dictionary with sub items like below.

* ```ballance``` : the balance of this wallet

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

* ```AddressIsWrong```: Address is wrong.

## ```get_balance()```

Get the balance of all addresses in the current wallet.

### Arguments

* N/A

### Successful case

* Return integer with decimal point 10^18.
Ex) 1.10 icx => It will return 1,100,000,000,000,000,000.

### Error cases

It will raise following exception.

* AddressIsWrong : Address is wrong.

## ```get_address()```

Get the address of wallet.

### Arguments

* N/A

### Successful case

* Return string of wallet address begins from ‘hx’.

### Error cases

It will raise following exception.

* ```AddressIsWrong``` : Address is wrong.
