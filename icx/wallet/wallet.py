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

import json
from eth_keyfile import create_keyfile_json, decode_keyfile_json
from icx.custom_error import PasswordIsNotAcceptable, FileExists, NoPermissionToWriteFile, FilePathIsWrong, \
    FilePathWithoutFileName, PasswordIsWrong
from icx.utils import validate_password, create_jsonrpc_request_content, \
        store_wallet, validate_key_store_file, read_wallet, \
        get_balance, validate_address, validate_address_is_not_same, check_amount_and_fee_is_valid, make_params, \
        request_generator, get_balance_after_trasfer, check_balance_enough, key_from_key_store
from icx.signer import IcxSigner


class Wallet:

    def __init__(self, wallet_data: dict=None, public_key=None, uri="https://testwallet.icon.foundation/api/", address: str=None):
        self.__wallet_info = wallet_data if wallet_data else wallet_data
        self.__address = self.__wallet_info["address"] if wallet_data else address          # an address of the wallet
        self.__public_key = public_key                                                      # a public key of the wallet
        self.__uri = uri                                                                    # a target uri for api

    @property
    def address(self):
        return self.__address

    @property
    def wallet_info(self):
        return self.__wallet_info

    @property
    def public_key(self):
        return self.__public_key

    @property
    def uri(self):
        return self.__uri

    @address.setter
    def address(self, address):
        self.__address = address

    @wallet_info.setter
    def wallet_info(self, wallet_info):
        self.__wallet_info = wallet_info

    @public_key.setter
    def public_key(self, public_key):
        self.__public_key = public_key

    @uri.setter
    def uri(self, uri):
        self.__uri = uri

    @staticmethod
    def create_keystore_file_of_wallet(keystore_file_path, password):
        """ create both a wallet and a keystore file

           :param keystore_file_path: File path for the keystore file of the wallet.
           :param password:  Password including alphabet character, number, and special character.

           :return: Instance of Wallet class.
        """
        if not validate_password(password):
            raise PasswordIsNotAcceptable

        try:
            signer = IcxSigner()
            byte_private_key = signer.private_key_bytes

            key_store_contents = create_keyfile_json(byte_private_key, bytes(password, 'utf-8'), iterations=262144)
            key_store_contents['address'] = "hx" + signer.address.hex()
            key_store_contents['coinType'] = 'icx'
            json_string_keystore_data = json.dumps(key_store_contents)
            store_wallet(keystore_file_path, json_string_keystore_data)

            wallet = Wallet(key_store_contents)
            return wallet, signer.private_key_bytes.hex()

        except FileExistsError:
            raise FileExists
        except PermissionError:
            raise NoPermissionToWriteFile
        except FileNotFoundError:
            raise FilePathIsWrong
        except IsADirectoryError:
            raise FilePathWithoutFileName

    @staticmethod
    def create_wallet_by_private_key(hex_private_key=None):
        """ create wallet without keystore file

           :param hex_private_key: the private key with a hexadecimal number

           :return: Instance of Wallet class.
           """
        byte_private_key, is_byte = None, None

        if hex_private_key:
            byte_private_key = bytes.fromhex(hex_private_key)
            is_byte = True

        try:

            signer = IcxSigner(byte_private_key, is_byte)

            wallet = Wallet()
            wallet.address = "hx" + signer.address.hex()

            return_value = (wallet, signer.private_key_bytes.hex())
            return return_value

        except TypeError:
            raise TypeError

    @staticmethod
    def open_keystore_file_of_wallet(keystore_file_path, password):
        """ open the keystore file and read the information of the file

            :param keystore_file_path: File path for the keystore file of the wallet.
            :param password:  Password including alphabet character, number, and special character.

            :return Instance of Wallet Class.
        """
        if not validate_password(password):
            raise PasswordIsNotAcceptable

        try:
            validate_key_store_file(keystore_file_path)
            private_key_bytes = key_from_key_store(keystore_file_path, bytes(password, 'utf-8'))
            wallet = Wallet(read_wallet(keystore_file_path))
            return_value = (wallet, private_key_bytes.hex())
            return return_value
        except FileNotFoundError:
            raise FilePathIsWrong
        except ValueError:
            raise PasswordIsWrong

    def transfer_value(self, password, to_address, value, fee=10000000000000000,
                       uri='https://testwallet.icon.foundation/api/', hex_private_key=None, **kwargs):
        """ transfer the specific value with private key

            :param password:  Password including alphabet character, number, and special character.
            :param to_address: Address of wallet to receive the asset.
            :param value: Amount of money.
            :param fee: Transaction fee.
            :param uri: Api url. type(str)
            :param hex_private_key: the private key with a hexadecimal number

            :return: response
        """
        try:

            uri = f'{uri}v2'
            byte_private_key = decode_keyfile_json(self.wallet_info, bytes(password, 'utf-8'))

            validate_address(to_address)
            validate_address(self.address)
            validate_address_is_not_same(to_address, self.address)

            method = 'icx_sendTransaction'
            value, fee = int(value), int(fee)

            check_amount_and_fee_is_valid(value, fee)

            params = make_params(self.address, to_address, value, fee, method, byte_private_key)
            payload = create_jsonrpc_request_content(0, method, params)

            # Request the balance repeatedly until we get the response from ICON network.
            request_gen = request_generator(uri)
            balance = get_balance_after_trasfer(self.address, uri, request_gen)
            check_balance_enough(balance, value, fee)
            next(request_gen)
            response = request_gen.send(payload)
            return response
        except FileNotFoundError:
            raise FilePathIsWrong
        except IsADirectoryError:
            raise FilePathIsWrong
        except ValueError:
            raise PasswordIsWrong

    def get_wallet_info(self, uri="https://testwallet.icon.foundation/api/"):
        """ get the keystore file information and the balance

            :param uri type(str)

            :return wallet information. type(dict)
        """
        balance = get_balance(self.address, uri)
        self.wallet_info['balance'] = balance
        return self.wallet_info

    def get_balance(self, uri="https://testwallet.icon.foundation/api/"):
        """ get the balance

            :param uri type(str)

            :return wallet information. type(dict)
        """
        balance = get_balance(self.address, uri)
        return balance

    def get_address(self):
        """ get the address
        """
        return self.address


