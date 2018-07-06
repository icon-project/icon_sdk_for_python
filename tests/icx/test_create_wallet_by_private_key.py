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
import time
from icx.wallet import Wallet


class TestCreateWalletByPrivateKey(unittest.TestCase):

    def test0(self):
        """ Case to create wallet successfully.
        """

        # Given, When
        wallet1, _ = Wallet.create_wallet_by_private_key('password1234*','71fc378d3a3fb92b57474af156f376711a8a89d277c9b60a923a1db75575b1cc')

        # Then
        self.assertIsNotNone(wallet1.wallet_info, 'wallet_info field is empty.')
        self.assertEqual(wallet1.address, "hxcc7b1f5fb98ca1eeaf9586bc08048814cb0d4d3d")

    def test0_1(self):
        """ Case to create wallet without private key successfully.
        """

        # Given, When
        wallet1, _ = Wallet.create_wallet_by_private_key('password1234*')

        # Then
        self.assertIsNotNone(wallet1.wallet_info, 'wallet_info field is empty.')

        # Given, When
        wallet2, _ = Wallet.create_wallet_by_private_key(
            'password1234*', "df7784bc856bc3e96d5b2733957ea0a47ff39d60aaf8a3406a74b8580e8395cc")

        # Then
        self.assertEqual(wallet2.address, "hx66425784bfddb5b430136b38268c3ce1fb68e8c5")
        self.assertIsNotNone(wallet2.wallet_info, 'wallet_info field is empty.')

        ret = bool(wallet2.transfer_value(
            'password1234*', to_address=wallet1.address,
            value="3300000000000000000", fee=10000000000000000))

        # Then
        self.assertEqual(True, ret)

        # Need to do wait for a while because it takes time to make consensus among nodes.
        # We recommend 0.3 sec at least.
        time.sleep(1)

        balance = wallet1.get_balance()
        self.assertIsNot(balance, 0, "Current balance is 0.")
        self.assertEqual(balance, 3300000000000000000, "Wallet balance is wrong.")

    def test1(self):
        """ Case the private key is not composed of 32 bytes.
        """
        try:
            # Given, When
            wallet1, _ = Wallet.create_wallet_by_private_key('password1234*', '71fc378d3a3fb92b57474af156f9d277c9b60a923a1db75575b1cc')

        # Then
        except TypeError:
            self.assertTrue(True)

    def test2(self):
        """ Case the private key is composed of 32 bytes and transfer icx successfully.
        """

        # Given, When
        wallet, _ = Wallet.create_wallet_by_private_key(
            'password1234*', "df7784bc856bc3e96d5b2733957ea0a47ff39d60aaf8a3406a74b8580e8395cc")

        # Then
        self.assertIsNotNone(wallet.wallet_info, 'wallet_info field is empty.')
        self.assertEqual(wallet.address, "hx66425784bfddb5b430136b38268c3ce1fb68e8c5")

        try:

            ret = bool(wallet.transfer_value(
                'password1234*', to_address="hxa974f512a510299b53c55535c105ed962fd01ee3",
                value="50000000000000000000", fee=10000000000000000))

            # Then
            self.assertEqual(True, ret)

        except FileNotFoundError:
            self.assertFalse(True)

    def test3(self):
        """ Case the private key is composed of 32 bytes and transfer several icx twice successfully.

        :return:
        """
        # Given, When
        wallet1, _ = Wallet.create_wallet_by_private_key(
            'password1234*', "df7784bc856bc3e96d5b2733957ea0a47ff39d60aaf8a3406a74b8580e8395cc")

        # Then
        self.assertEqual(wallet1.address, "hx66425784bfddb5b430136b38268c3ce1fb68e8c5")
        self.assertIsNotNone(wallet1.wallet_info, 'wallet_info field is empty.')

        wallet2, _ = Wallet.create_wallet_by_private_key(
            'password1234*', "71fc378d3a3fb92b57474af156f376711a8a89d277c9b60a923a1db75575b1cc")

        # Then
        self.assertIsNotNone(wallet2.wallet_info, 'wallet_info field is empty.')
        self.assertEqual(wallet2.address, "hxcc7b1f5fb98ca1eeaf9586bc08048814cb0d4d3d")

        try:

            ret = bool(wallet1.transfer_value(
                'password1234*', to_address="hxcc7b1f5fb98ca1eeaf9586bc08048814cb0d4d3d",
                value="533000000000000000", fee=10000000000000000))

            # Then
            self.assertEqual(True, ret)
            # Then
            self.assertEqual(True, ret)

            ret2 = bool(wallet2.transfer_value(
                'password1234*', to_address="hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
                value="22200000000000000", fee=10000000000000000))
            # Then
            self.assertEqual(True, ret2)

        except FileNotFoundError:
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()
