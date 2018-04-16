import unittest
import os
import requests
requests.packages.urllib3.disable_warnings()
from icx.wallet.wallet import Wallet
from icx.custom_error import FilePathIsWrong

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))


class TestGetAddress(unittest.TestCase):

    def test0(self):
        """ Case to verify the wallet address from the wallet generated from private key
        """

        wallet = Wallet.create_wallet_by_private_key('71fc378d3a3fb92b57474af156f376711a8a89d277c9b60a923a1db75575b1cc')
        self.assertEqual(wallet.get_address(), "hxcc7b1f5fb98ca1eeaf9586bc08048814cb0d4d3d")

    def test1(self):
        """ Case to get an address successfully on creating a keystore file of wallet
        """

        file_path = os.path.join(TEST_DIR, "test_keystore.txt")
        if os.path.isfile(file_path):
            os.remove(file_path)

        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            wallet = Wallet.create_keystore_file_of_wallet(keystore_file_path, password)

            prefix = wallet.get_address()[0:2]
            self.assertEqual(prefix, "hx")

        except FileExistsError:
            self.assertFalse(True)
        except FilePathIsWrong:
            self.assertFalse(True)

    def test2(self):
        """ Case to get an address successfully on opening a keystore file of wallet.
        """

        password = "Adas21312**"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)

            prefix = wallet.get_address()[0:2]
            self.assertEqual(prefix, "hx")

        except FileNotFoundError:
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()
