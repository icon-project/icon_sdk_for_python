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
import json
from icx.custom_error import FilePathIsWrong, PasswordIsWrong, NotEnoughBalanceInWallet, TransferFeeIsInvalid, \
    AddressIsWrong, FeeIsBiggerThanAmount, AmountIsInvalid, AddressIsSame, PasswordIsNotAcceptable
from icx.wallet.wallet import Wallet

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))


class TestTransferValue(unittest.TestCase):

    def test0(self):
        """ Case when succeed transfer value.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = bool(wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=10000000000000000))

            # Then
            self.assertEqual(True, ret)

        except FileNotFoundError:
            self.assertFalse(True)

    def test1(self):
        """ Case when key_store_file_path is wrong.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "./wrong_path")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="10000000000000000000", fee=10000000000000000)

        # Then
        except FilePathIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test2_1(self):
        """ Case when password is not acceptable.
        """
        # Given
        password = "wrong_password"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=10000000000000000)

        # Then
        except PasswordIsNotAcceptable:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test2_2(self):
        """ Case when password is wrong.
        """
        # Given
        password = "wrong_password123"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=10000000000000000)

        # Then
        except PasswordIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test3(self):
        """ Case when wallet does not have enough balance.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="10000000000000000000000000000000000000000000000000", fee=10000000000000000)

        # Then
        except NotEnoughBalanceInWallet:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test4(self):
        """ Case when transfer fee is invalid.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=100000000000)

        # Then
        except TransferFeeIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test5(self):
        """ Case when wallet address is wrong.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet, _= Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed9",
                value="1000000000000000000", fee=10000000000000000)

        # Then
        except AddressIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test6(self):
        """ Case when Fee is not 10000000000000000.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="11234440000000000000", fee=100000000000000)

        # Then
        except TransferFeeIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test7(self):
        """ Case when Fee is bigger than Amount.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000", fee=10000000000000000)

        # Then
        except FeeIsBiggerThanAmount:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test8(self):
        """ Case when Amount is 0.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="0", fee=10000000000000000)

        # Then
        except AmountIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test9(self):
        """ Case when balance is same as sum of Amount and Fee.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path1 = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            # When
            wallet1, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path1, password)

            # send the value to the address of keystore file (test_keystore_for_transfer2)
            ret = wallet1.transfer_value(
                password, to_address="hx95e12b1f98f9b847175849f51bed5d121e742f6a",
                value="1010000000000000000", fee=10000000000000000)

            password = "Adas21312**"
            keystore_file_path2 = os.path.join(TEST_DIR, "test_keystore_for_transfer2.txt")
            wallet2, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path2, password)
            ret = wallet2.transfer_value(
                password, to_address="hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
                value="1000000000000000000", fee=10000000000000000)
            print(ret.json())
        # Then
        except AmountIsInvalid:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test10(self):
        """ Case when wallet address to transfer is same as wallet address to be sent.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            # When
            wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
                value="0", fee=10000000000000000)

        # Then
        except AddressIsSame:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
