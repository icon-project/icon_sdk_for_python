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

import hashlib
import base64
from icx.signer import IcxSigner


def sha3_256(data):
    """Get hash value using sha3_256 hash function.

    :param data:
    :return: 256 bit hash value (32 bytes). type(bytes).
    """
    return hashlib.sha3_256(data).digest()


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


def get_tx_hash(method, params):
    """Create tx_hash from params object.

    :param method: Method name. type(str)
    :param params: The value of 'params' key in jsonrpc.
    :return: bytes: sha3_256 hash value
    """

    tx_phrase = get_tx_phrase(method, params)
    return sha3_256(tx_phrase.encode())


def get_tx_phrase(method, params):
    """Create tx phrase from method and params. tx_phrase means input text to create tx_hash.

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
    """Create params phrase recursively."""
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
