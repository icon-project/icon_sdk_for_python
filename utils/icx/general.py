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

import re
import time
import certifi
import requests
from icx.custom_error import NotEnoughBalanceInWallet, AmountIsInvalid, TransferFeeIsInvalid, FeeIsBiggerThanAmount


def hex_to_bytes(value) -> bytes:
    return bytes.fromhex(value)


def bytes_to_hex(value):
    return value.hex()


def get_timestamp_us() -> int:
    """Get epoch time in us."""
    return int(time.time() * 10 ** 6)


def validate_password(password) -> bool:
    """Validate a entered password.

    :param password: A password of keystore file. type(str).
    :return: bool.
    True: When the password is valid format.
    False: When the password is invalid format.
    """
    return bool(re.match(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+{}:<>?]).{8,}$', password))


def has_keys(dict_data, key_array) -> bool:
    """Check dictionary data has all key in array."""
    for key in key_array:
        if key in dict_data.keys():
            pass
        else:
            return False
    return True


def check_balance_enough(balance, amount, fee):
    """Check an user has enough balance to transfer.

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


def post(url, payload):
    try:
        path = certifi.where()
        r = requests.post(url, json=payload, verify=path)
        return r
    except requests.exceptions.Timeout:
        raise RuntimeError("Timeout happened. Check your internet connection status.")

