import unittest
import os
import requests
requests.packages.urllib3.disable_warnings()
from icx.wallet.wallet import Wallet
from icx.custom_error import FilePathIsWrong, PasswordIsWrong

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))


class TestOpenKeystoreFileOfWallet(unittest.TestCase):

    def test0(self):
        """ Case to open wallet successfully.
        """

        # Given
        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

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

        # When
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

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

        # When
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

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
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            self.assertTrue(type(wallet.wallet_info) == dict)
        finally:
            pass


if __name__ == "__main__":
    unittest.main()

