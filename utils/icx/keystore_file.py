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

import os
import codecs
import json
from eth_keyfile import create_keyfile_json, extract_key_from_keyfile, load_keyfile
from json import JSONDecodeError
from icx.custom_error import NotAKeyStoreFile
from .general import has_keys
from icx.signer import IcxSigner


def validate_key_store_file(key_store_file_path: object) -> bool:
    """Check key_store file was saved in the correct format.

    :param key_store_file_path:
    :return: type(bool).
    True: When the key_store_file was saved in valid format.
    False: When the key_store_file was saved in invalid format.
    """
    # The key values ​​that should be in the root location.
    root_keys = ["version", "id", "address", "crypto"]
    crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
    crypto_cipherparams_keys = ["iv"]
    crypto_kdfparams_keys = ["dklen", "salt", "c", "prf"]

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


def validate_wallet_info(wallet_info: dict) -> bool:
    """Check a wallet info has the right format or not.

    :param wallet_info:
    :return: type(bool).
    True: When the wallet info is in the correct format.
    False: When the wallet info is in the incorrect format.
    """
    root_keys = ["version", "id", "address", "crypto", "balance"]
    crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
    crypto_cipherparams_keys = ["iv"]
    crypto_kdfparams_keys = ["dklen", "salt", "c", "prf"]

    is_valid = has_keys(wallet_info, root_keys) and has_keys(wallet_info["crypto"], crypto_keys) and \
               has_keys(wallet_info["crypto"]["cipherparams"], crypto_cipherparams_keys) and \
               has_keys(wallet_info["crypto"]["kdfparams"], crypto_kdfparams_keys)
    return is_valid


def make_key_store_content(password):
    """Make a content of key_store.

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
    """Extract a private key from the keystore file.

    :param file_path:
    :return: private key.
    """
    with open(file_path, 'rb') as file:
        private_key = extract_key_from_keyfile(file, password)
    return private_key


def read_wallet(file_path):
    """Read keystore file.

    :param file_path:
    :return: wallet_info
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError
    with codecs.open(file_path, 'r', 'utf-8-sig') as f:
        wallet_info = json.load(f)
        f.close()

    return wallet_info


def store_wallet(file_path, json_string):
    """Store wallet information file in JSON format.

    :param file_path: The path where the file will be saved. type: str
    :param json_string: Contents of key_store_file
    """
    if os.path.isfile(file_path):
        raise FileExistsError
    with open(file_path, 'wt') as f:
        f.write(json_string)



