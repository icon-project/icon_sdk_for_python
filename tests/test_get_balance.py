import os
import unittest
from icx.wallet.wallet import Wallet
from icx.utils import change_hex_balance_to_decimal_balance
import requests
requests.packages.urllib3.disable_warnings()

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))

uri = 'https://testwallet.icon.foundation/api/'


class TestGetBalance(unittest.TestCase):

    def test_change_hex_balance_to_decimal_balance_case0(self):
        """ Case to return the right balance.
        """
        # Given
        hex_balance = '0x10e8205bae65f770000'
        dec_balance = '4989.990000000000000000'

        # When
        result_dec_balance = change_hex_balance_to_decimal_balance(hex_balance)

        # Then
        self.assertEqual(result_dec_balance, dec_balance)

    def test_change_hex_balance_to_decimal_balance_case1(self):
        """ Case to return the wrong balance.
        """
        # Given
        hex_balance = '0x10e8205bae65f770000'
        dec_balance = '4989.9900000000000001235'

        # When
        result_dec_balance = change_hex_balance_to_decimal_balance(hex_balance)

        # Then
        self.assertNotEqual(result_dec_balance, dec_balance)

    def test0(self):
        """ Case to get balance successfully that balance is 0.
        """
        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
        balance = wallet.get_balance(uri)

        # Then
        self.assertTrue(type(balance) == int)

    def test1(self):
        """ Case to get balance successfully that balance is more than 0.
        """
        # Given
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        # When
        wallet, _ = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
        balance = wallet.get_balance(uri)

        # Then
        self.assertTrue(type(balance) == int and balance > 0)


if __name__ == "__main__":
    unittest.main()

