#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 theloop Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import hashlib
import re
import time
import os
import codecs
import json
from eth_keyfile import create_keyfile_json, extract_key_from_keyfile, load_keyfile
from json import JSONDecodeError
import requests
from icx.custom_error import NotEnoughBalanceInWallet, AmountIsInvalid, AddressIsWrong, TransferFeeIsInvalid, \
    FeeIsBiggerThanAmount, NotAKeyStoreFile, AddressIsSame
from icx.signer import IcxSigner


def validate_password(password) -> bool:
    """ Verify the entered password.

    :param password: The password the user entered. type(str)

    :return: bool
    True: When the password is valid format
    False: When the password is invalid format
    """
    return bool(re.match(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+{}:<>?]).{8,}$', password))


def hex_to_bytes(value):
    return bytes.fromhex(value)


def bytes_to_hex(value):
    return value.hex()


def get_timestamp_us():
    """Get epoch time in us.
    """
    return int(time.time() * 10 ** 6)


def validate_address(address) -> bool:
    try:
        if len(address) == 42 and address.startswith('hx'):
            return True
        raise AddressIsWrong
    except ValueError:
        raise AddressIsWrong


def validate_address_is_not_same(to_address, from_address) -> bool:
    if to_address != from_address:
        return True
    else:
        raise AddressIsSame


def validate_key_store_file(key_store_file_path: object) -> bool:
    """ Check key_store file was saved in the correct format.

    :return: bool
    True: When the key_store_file was saved in valid format.
    False: When the key_store_file was saved in invalid format.
    """
    is_valid = True

    # The key values ​​that should be in the root location.
    root_keys = ["version", "id", "address", "crypto"]
    crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
    crypto_cipherparams_keys = ["iv"]
    crypto_kdfparams_keys = ["dklen", "salt", "c", "prf"]
    is_valid = False

    try:
        with open(key_store_file_path, 'rb') as key_store_file:
            key_file = load_keyfile(key_store_file)
        is_valid = has_keys(key_file, root_keys) and has_keys(key_file["crypto"], crypto_keys) and has_keys(key_file["crypto"]["cipherparams"], crypto_cipherparams_keys) and has_keys(key_file["crypto"]["kdfparams"], crypto_kdfparams_keys)
    except KeyError:
        raise NotAKeyStoreFile
    except JSONDecodeError:
        raise NotAKeyStoreFile
    if is_valid is not True:
        raise NotAKeyStoreFile
    return is_valid


def has_keys(data, key_array):
    for key in key_array:
        if key in data is False:
            return False
    return True


def sha3_256(data):
    """ Get hash value using sha3_256 hash function.

    :param data:
    :return: 256bit hash value (32 bytes). type(bytes)
    """
    return hashlib.sha3_256(data).digest()


def get_address_by_privkey(privkey_bytes):
    """ Get address by Private key.

    :param privkey_bytes: Private key. type(string)
    """
    account = IcxSigner.from_bytes(privkey_bytes)
    return f'hx{bytes_to_hex(account.address)}'


def get_tx_hash(method, params):
    """ Create tx_hash from params object.

    :param method: Method name. type(str)
    :param params: The value of 'params' key in jsonrpc.

    :return: bytes: sha3_256 hash value
    """

    tx_phrase = get_tx_phrase(method, params)
    return sha3_256(tx_phrase.encode())


def get_tx_phrase(method, params):
    """ Create tx phrase from method and params. tx_phrase means input text to create tx_hash.

    :param method: The value of 'params' key in jsonrpc. type(dict)
    :param params: Method name. type(str)

    :return: sha3_256 hash format without '0x' prefix
    """
    keys = [key for key in params]

    key_count = len(keys)
    if key_count == 0:
        return method

    phrase = get_params_phrase(params)

    return f'{method}.{phrase}'


def get_params_phrase(params):
    """Create params phrase recursively
    """
    keys = [key for key in params]
    keys.sort()
    key_count = len(keys)
    if key_count == 0:
        return ""
    phrase = ""

    if isinstance(params[keys[0]], dict) is not True:
        phrase += f'{keys[0]}.{params[keys[0]]}'
    elif bool(params[keys[0]]) is not True:
        phrase += f'{keys[0]}'
    else:
        phrase += f'{keys[0]}.{get_params_phrase(params[keys[0]])}'

    for i in range(1, key_count):
        key = keys[i]

        if isinstance(params[key], dict) is not True:
            phrase += f'.{key}.{params[key]}'
        elif bool(params[key]) is not True:
            phrase += f'.{key}'
        else:
            phrase += f'.{key}.{get_params_phrase(params[key])}'

    return phrase


def sign_recoverable(private_key_bytes, tx_hash_bytes):
    """
    :param private_key_bytes: Byte private key value.
    :param tx_hash_bytes: 32 byte tx_hash data. type(bytes)
    :return: signature_bytes + recovery_id(1)
    """
    signer = IcxSigner.from_bytes(private_key_bytes)
    signature_bytes, recovery_id = signer.sign_recoverable(tx_hash_bytes)

    # append recover_id(1 byte) to signature_bytes.
    return bytes(bytearray(signature_bytes) + recovery_id.to_bytes(1, 'big'))


def sign(private_key_bytes, tx_hash_bytes):
    """
    :param private_key_bytes:
    :param tx_hash_bytes:
    :return: base64-encoded string of recoverable signature data
    """

    recoverable_sig_bytes = sign_recoverable(private_key_bytes, tx_hash_bytes)
    return base64.b64encode(recoverable_sig_bytes)


def create_jsonrpc_request_content(_id, method, params):

    content = {
        'jsonrpc': '2.0',
        'method': method,
        'id': _id
    }

    if params is not None:
        content['params'] = params

    return content


def post(url, payload):
    try:
        r = requests.post(url, json=payload, verify=False)
        return r
    except requests.exceptions.Timeout:
        raise RuntimeError("Timeout happened. Check your internet connection status.")


def get_payload_of_json_rpc_get_balance(address, url):

    method = 'icx_getBalance'
    params = {'address': address}
    payload = create_jsonrpc_request_content(0, method, params)
    return payload


def check_balance_enough(balance, amount, fee):
    """ Check if the user has enough balance to transfer.

    :param balance: Balance of the user's wallet.
    :param amount: Amount of money. type(str)
    :param fee: Transfer fee.

    :return: True when the user has enough balance.
    """
    if balance >= amount + fee:
        return True
    else:
        raise NotEnoughBalanceInWallet
    pass


def check_amount_and_fee_is_valid(amount, fee):
    if amount <= 0:
        raise AmountIsInvalid
    if fee <= 0 or fee != 10000000000000000:
        raise TransferFeeIsInvalid
    if amount < fee:
        raise FeeIsBiggerThanAmount


def change_hex_balance_to_decimal_balance(hex_balance, place=18):
    """ Change hex balance to decimal decimal icx balance.

    :param: hex_balance

    :return: result_decimal_icx: string decimal icx
    """
    dec_balance = int(hex_balance, 16)
    str_dec_balance = str(dec_balance)
    if dec_balance >= 10 ** place:
        str_int = str_dec_balance[:len(str_dec_balance) - place]
        str_decimal = str_dec_balance[len(str_dec_balance) - place:]
        result_decimal_icx = f'{str_int}.{str_decimal}'
        return result_decimal_icx

    else:
        zero = "0."
        val_point = len(str_dec_balance)
        point_difference = place - val_point
        str_zero = "0" * point_difference
        result_decimal_icx = f'{zero}{str_zero}{dec_balance}'
        return result_decimal_icx


def request_generator(url):
    while True:
        payload = yield
        yield post(url, payload)


def make_params(user_address, to, amount, fee, method, private_key_bytes):
    """ Make params for jsonrpc format.

    :param user_address: Address of user's wallet.
    :param to: Address of wallet to receive the asset.
    :param amount: Amount of money.
    :param fee: Transaction fee.
    :param method: Method type. type(str)
    :param private_key_bytes: Private key of user's wallet.

    :return: type(dict)
    """
    params = {
        'from': user_address,
        'to': to,
        'value': hex(amount),
        'fee': hex(fee),
        'timestamp': str(get_timestamp_us())
    }
    tx_hash_bytes = get_tx_hash(method, params)
    signature_bytes = sign(private_key_bytes, tx_hash_bytes)
    params['tx_hash'] = tx_hash_bytes.hex()
    params['signature'] = signature_bytes.decode()

    return params


def store_wallet(file_path, json_string):
    """ Store wallet information file in JSON format.

    :param file_path: The path where the file will be saved. type: str
    :param json_string: Contents of key_store_file
    """
    if os.path.isfile(file_path):
        raise FileExistsError

    with open(file_path, 'wt') as f:
        f.write(json_string)


def make_key_store_content(password):
    """ Make a content of key_store.

    :param password: Password including alphabet character, number, and special character.

    :return: key_store_content(dict)
    """
    signer = IcxSigner()
    private_key = signer.private_key
    key_store_contents = create_keyfile_json(private_key, bytes(password, 'utf-8'), iterations=262144)
    icx_address = "hx" + signer.address.hex()
    key_store_contents['address'] = icx_address
    key_store_contents['coinType'] = 'icx'
    return key_store_contents


def key_from_key_store(file_path, password):
    """

    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as file:
        private_key = extract_key_from_keyfile(file, password)
    return private_key


def get_balance(address, url):
    """ Get balance of the address indicated by address.

    :param address: icx account address starting with 'hx'
    :param url:

    :return: icx
    """
    url = f'{url}v2'

    method = 'icx_getBalance'
    params = {'address': address}
    payload = create_jsonrpc_request_content(0, method, params)
    response = post(url, payload)
    content = response.json()
    hex_balance = content['result']['response']
    dec_loop_balance = int(hex_balance, 16)

    return dec_loop_balance


def read_wallet(file_path):
    """Read keystore file

    :param file_path:

    :return: wallet_info
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError
    with codecs.open(file_path, 'r', 'utf-8-sig') as f:
        wallet_info = json.load(f)
        f.close()

    return wallet_info


def get_balance_after_trasfer(address, url, request_gen):
    """ Get balance of the address indicated by address for check balance before transfer icx.

    :param address: Icx account address starting with 'hx'
    :param url: Api url. type(str)
    :param request_gen:

    :return: Balance of the user's wallet.
    """
    payload_for_balance = get_payload_of_json_rpc_get_balance(address, url)

    next(request_gen)
    balance_content = request_gen.send(payload_for_balance).json()

    balance = balance_content['result']['response']
    balance_loop = int(balance, 16)
    return balance_loop
