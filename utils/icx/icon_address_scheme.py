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

from icx.custom_error import AddressIsSame, AddressIsWrong
from icx.signer import IcxSigner


def validate_address(address) -> bool:
    """Check address length is right and it starts with 'hx'.

    :param address: an address of a wallet.
    :return: type(bool).
    """
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


def get_address_by_privkey(privkey_bytes):
    """Get address by Private key.

    :param privkey_bytes: Private key. type(string).
    """
    account = IcxSigner.from_bytes(privkey_bytes)
    return f'hx{bytes_to_hex(account.address)}'

