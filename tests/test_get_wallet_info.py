import os
import unittest
import requests
requests.packages.urllib3.disable_warnings()
from icx.wallet.wallet import Wallet

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))

api_url = 'https://testwallet.icon.foundation/api/'


class TestGetWalletInfo(unittest.TestCase):

    def test0(self):
        """ Case when returning the wallet address successfully.
        """

        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:

            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(api_url)

            prefix = wallet_info['address'][0:2]
            self.assertEqual(prefix, "hx")

        except FileNotFoundError:
            self.assertFalse(True)

    def test3(self):
        """ Case when returning the balance successfully.
        """

        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(api_url)
            balance = wallet_info['balance']

            self.assertTrue(type(balance) == int)
        finally:
            pass

    def test4(self):
        """ Case when returning the wallet info in keystore file successfully.
        """

        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            wallet_info = wallet.get_wallet_info(api_url)

            self.assertTrue(type(wallet_info) == dict)
        finally:
            pass


if __name__ == "__main__":
    unittest.main()