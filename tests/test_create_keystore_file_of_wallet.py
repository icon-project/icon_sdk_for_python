import unittest
import os
import json
from icx.wallet.wallet import Wallet
from icx.custom_error import FilePathIsWrong, PasswordIsNotAcceptable, NoPermissionToWriteFile, FileExists, NotAKeyStoreFile
from icx.utils import validate_key_store_file

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/test_keystore.txt"))


class TestCreateWalletAndKeystoreFile(unittest.TestCase):

    def setUp(self):
        # Remove used file.
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")
        if os.path.isfile(file_path):
            os.remove(file_path)

    def test0(self):
        """ Case to create wallet successfully.
        """
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            wallet1 = Wallet.create_keystore_file_of_wallet(file_path, password)[0]
            # Then
            prefix = wallet1.address[0:2]
            self.assertEqual(prefix, "hx")

        except FilePathIsWrong:
            self.assertFalse(True)
        except PasswordIsNotAcceptable:
            self.assertFalse(True)
        except NoPermissionToWriteFile:
            self.assertFalse(True)

        # Remove used file.
        os.remove(file_path)

    def test1(self):
        """ Case to enter a directory that does not exist.
        """
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, 'unknown', "test_keystore.txt")

        try:
            wallet1 = Wallet.create_keystore_file_of_wallet(file_path, password)
        except FilePathIsWrong:
            self.assertTrue(True)

    def test2(self):
        """ Case to enter a invalid password.
        """
        password = "123 4"
        file_path = os.path.join(TEST_DIR, "unknown_folder", "test_keystore.txt")

        try:
            wallet1 = Wallet.create_keystore_file_of_wallet(file_path, password)
        except PasswordIsNotAcceptable:
            self.assertTrue(True)

    def test3(self):
        """ Case to enter a directory without permission to write file.
        """
        password = "Adas21312**"
        file_path = os.path.join("/", "test_keystore.txt")

        try:
            wallet1 = Wallet.create_keystore_file_of_wallet(file_path, password)
        except NoPermissionToWriteFile:
            self.assertTrue(True)

    def test4(self):
        """ Case to overwrite keystore file.
        """
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        wallet1 = Wallet.create_keystore_file_of_wallet(file_path, password)

        try:
            wallet2 = Wallet.create_keystore_file_of_wallet(file_path, password)
        except FileExists:  # Raise exception that file exists.
            self.assertTrue(True)

            # Remove used file.
            os.remove(file_path)

    def test5(self):
        """ Case to enter the file, not a key_store_file.
        """
        file_path = os.path.join(TEST_DIR, "not_a_key_store_file.txt")\

        try:
            wallet1 = validate_key_store_file(file_path)
        except NotAKeyStoreFile:
            self.assertTrue(True)

    def test6(self):
        """ Case to save the file in the correct format.
        """
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        wallet1 = Wallet.create_keystore_file_of_wallet(file_path, password)
        self.assertTrue(validate_key_store_file(file_path))


if __name__ == "__main__":
    unittest.main()
