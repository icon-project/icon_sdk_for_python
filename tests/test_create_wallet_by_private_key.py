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
from icx.wallet.wallet import Wallet


class TestCreateWalletByPrivateKey(unittest.TestCase):

    def test0(self):
        """ Case to create wallet successfully.
        """

        # Given, When
        wallet1, _ = Wallet.create_wallet_by_private_key('71fc378d3a3fb92b57474af156f376711a8a89d277c9b60a923a1db75575b1cc')

        # Then
        self.assertEqual(wallet1.address, "hxcc7b1f5fb98ca1eeaf9586bc08048814cb0d4d3d")

    def test1(self):
        """ Case the private key is not composed of 32 bytes.
        """
        try:
            # Given, When
            wallet1, _ = Wallet.create_wallet_by_private_key('71fc378d3a3fb92b57474af156f9d277c9b60a923a1db75575b1cc')

        # Then
        except TypeError:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
