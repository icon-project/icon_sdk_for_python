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
import unittest
from icx.wallet import Wallet
from utils.icx import validate_wallet_info

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))

uri = 'https://testwallet.icon.foundation/api/'


class TestGetWalletInfo(unittest.TestCase):

    def test0(self):
        """ Case to return the wallet address successfully.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(uri)

            # Then
            prefix = wallet_info['address'][0:2]
            self.assertEqual(prefix, "hx")
        except FileNotFoundError:
            self.assertFalse(True)

    def test1(self):
        """ Case to return the balance successfully.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(uri)

            # Then
            balance = wallet_info['balance']
            self.assertTrue(type(balance) == int)
        except FileNotFoundError:
            self.assertFalse(True)

    def test2(self):
        """ Case to return the wallet info in keystore file successfully.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(uri)

            # Then
            self.assertTrue(type(wallet_info) == dict)
        except FileNotFoundError:
            self.assertFalse(True)

    def test3(self):
        """ Case to return the correct form of wallet information.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(uri)

            # Then
            self.assertTrue(validate_wallet_info(wallet_info))
        except FileNotFoundError:
            self.assertFalse(True)

    def test4(self):
        """ Case to return the incorrect form of wallet information.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(uri)
            del wallet_info["address"]

            # Then
            self.assertFalse(validate_wallet_info(wallet_info))
        except FileNotFoundError:
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()
