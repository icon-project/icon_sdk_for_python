import os
import unittest
from icx.utils import get_tx_hash, sign
from icx.custom_error import FilePathIsWrong, PasswordIsWrong, NotEnoughBalanceInWallet, TransferFeeIsInvalid, \
    AddressIsWrong, FeeIsBiggerThanAmount, AmountIsInvalid, AddressIsSame, PasswordIsNotAcceptable
from icx.wallet.wallet import Wallet

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/not_a_key_store_file.txt"))


class TestTransferValue(unittest.TestCase):

    def test_get_tx(self):
        """ Test for get_tx_hash function.
        """
        method = "method"
        params = {"param1": 1}

        expect = b'\xc0\x84\x19o\xd3\xe6<\x9e%\xd9\x05\xd4\x8di\x17\xd3\x02<a\xc6\xa2\xb2\xec I-\x12\xe1n\xd5\xac:'
        tx_hash = get_tx_hash(method, params)

        self.assertEqual(expect, tx_hash)

    def test_sign(self):
        """ Test for sign function.
        """
        tx_hash = b'\xc0\x84\x19o\xd3\xe6<\x9e%\xd9\x05\xd4\x8di\x17\xd3\x02<a\xc6\xa2\xb2\xec I-\x12\xe1n\xd5\xac:'
        private_key_bytes = b'x\xf3\xda\xdc\x80h\xf3hc`L\x1f\xc4Y\x83z@\xa2Mn$\x94\x16\x01\x83\x9cYp\x1d,\x93\xdd'

        expect = b'qeTA6B2VssGxrSE+SlOjRm0/RbqB9OKo2VHrgL7kVCUklcltf3AUeiujpWVAZXwZjPWmND1oyFStC00BHbQXVAA='
        signature_bytes = sign(private_key_bytes, tx_hash)

        self.assertEqual(expect, signature_bytes)

    def test0(self):
        """ Case when succeed transfer value.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = bool(wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=10000000000000000))

            self.assertEqual(True, ret)

        except FileNotFoundError:
            self.assertFalse(True)

    def test1(self):
        """ Case when key_store_file_path is wrong.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "./wrong_path")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="10000000000000000000", fee=10000000000000000)

        except FilePathIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test2_1(self):
        """ Case when password is not acceptable.
        """
        password = "wrong_password"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=10000000000000000)

        except PasswordIsNotAcceptable:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test2_2(self):
        """ Case when password is wrong.
        """
        password = "wrong_password123"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=10000000000000000)

        except PasswordIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test3(self):
        """ Case when wallet does not have enough balance.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="10000000000000000000000000000000000000000000000000", fee=10000000000000000)

        except NotEnoughBalanceInWallet:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test4(self):
        """ Case when transfer fee is invalid.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000000", fee=100000000000)

        except TransferFeeIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test5(self):
        """ Case when wallet address is wrong.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed9",
                value="1000000000000000000", fee=10000000000000000)

        except AddressIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test6(self):
        """ Case when Fee is not 10000000000000000.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="11234440000000000000", fee=100000000000000)

        except TransferFeeIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test7(self):
        """ Case when Fee is bigger than Amount.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="1000000000000000", fee=10000000000000000)

        except FeeIsBiggerThanAmount:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test8(self):
        """ Case when Amount is 0.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hxa974f512a510299b53c55535c105ed962fd01ee2",
                value="0", fee=10000000000000000)

        except AmountIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test9(self):
        """ Case when balance is same as sum of Amount and Fee.
        """
        password = "ejfnvm1234*"
        keystore_file_path1 = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            wallet1 = Wallet.open_keystore_file_of_wallet(keystore_file_path1, password)
            ret = wallet1.transfer_value(
                password, to_address="hx95e12b1f98f9b847175849f51bed5d121e742f6a",
                value="1020000000000000000", fee=10000000000000000)

            password = "Adas21312**"
            keystore_file_path2 = os.path.join(TEST_DIR, "test_keystore_for_transfer2.txt")
            wallet2 = Wallet.open_keystore_file_of_wallet(keystore_file_path2, password)
            ret = wallet2.transfer_value(
                password, to_address="hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
                value="1000000000000000000", fee=10000000000000000)

        except AmountIsInvalid:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test10(self):
        """ Case when wallet address to transfer is same as wallet address to be sent.
        """
        password = "ejfnvm1234*"
        keystore_file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            wallet = Wallet.open_keystore_file_of_wallet(keystore_file_path, password)
            ret = wallet.transfer_value(
                password, to_address="hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
                value="0", fee=10000000000000000)

        except AddressIsSame:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
