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

from .general import get_timestamp_us, post
from .signature import sign, get_tx_hash


def create_jsonrpc_request_content(_id, method, params):

    content = {
        'jsonrpc': '2.0',
        'method': method,
        'id': _id
    }

    if params is not None:
        content['params'] = params

    return content


def get_payload_of_json_rpc_get_balance(address, url):
    method = 'icx_getBalance'
    params = {'address': address}
    payload = create_jsonrpc_request_content(0, method, params)
    return payload


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


def get_balance(address, url):
    """ Get balance of the address indicated by address.

    :param address: icx account address starting with 'hx'
    :param url: api target url

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


def get_block_by_hash(hash, url):
    """ Get block information by hash.

    :param hash: Using hash values ​​with electronic signatures. 64 character. hexadecimal.
    :param url: api target url

    :return: response result(json)
    """
    url = f'{url}v2'

    method = 'icx_getBlockByHash'
    params = {'hash': hash}
    payload = create_jsonrpc_request_content(0, method, params)
    response = post(url, payload)
    json_response = response.json()
    return json_response


def get_block_by_height(height, url):
    """ Get block information by height.

    :param height: block's height
    :param url: api target url

    :return: response result(json)
    """
    url = f'{url}v2'

    method = 'icx_getBlockByHeight'
    params = {'height': height}
    payload = create_jsonrpc_request_content(0, method, params)
    response = post(url, payload)
    json_response = response.json()
    return json_response


def get_last_block(url):
    """ Get last block information.

    :param url: api target url

    :return: response result(json)
    """
    url = f'{url}v2'

    method = 'icx_getLastBlock'
    params = {}
    payload = create_jsonrpc_request_content(0, method, params)
    response = post(url, payload)
    json_response = response.json()
    return json_response


def get_balance_after_trasfer(address, uri, request_gen):
    """ Get balance of the address indicated by address for check balance before transfer icx.

    :param address: Icx account address starting with 'hx'
    :param uri: Api uri. type(str)
    :param request_gen:

    :return: Balance of the user's wallet.
    """
    payload_for_balance = get_payload_of_json_rpc_get_balance(address, uri)

    next(request_gen)
    balance_content = request_gen.send(payload_for_balance).json()

    balance = balance_content['result']['response']
    balance_loop = int(balance, 16)
    return balance_loop
