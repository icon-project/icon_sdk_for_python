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

import unittest
import os
from icx.wallet import Wallet
from icx.custom_error import FilePathIsWrong, PasswordIsWrong

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))


class TestOpenKeystoreFileOfWallet(unittest.TestCase):

    def test0(self):
        """ Case to open wallet successfully.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

            # Then
            prefix = wallet.address[0:2]
            self.assertEqual(prefix, "hx")
        except FileNotFoundError:
            self.assertFalse(True)

    def test1(self):
        """ Case to enter a directory that does not exist.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "unknown_folder", "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

        # Then
        except FilePathIsWrong:
            self.assertTrue(True)
        except FileNotFoundError:
            self.assertTrue(True)

    def test2(self):
        """ Case to enter a invalid password.
        """
        # Given
        password = "1234**wrongpassword"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

        # Then
        except PasswordIsWrong:
            self.assertTrue(True)

    def test3(self):
        """ Case to return the wallet info in keystore file successfully.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

        # Then
        self.assertTrue(type(wallet.wallet_info) == dict)


if __name__ == "__main__":
    unittest.main()

