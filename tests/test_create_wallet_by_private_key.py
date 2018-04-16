import unittest
from icx.wallet.wallet import Wallet


class TestCreateWalletByPrivateKey(unittest.TestCase):

    def test0(self):
        """ Case to create wallet successfully.
        """
        wallet1 = Wallet.create_wallet_by_private_key('71fc378d3a3fb92b57474af156f376711a8a89d277c9b60a923a1db75575b1cc')
        self.assertEqual(wallet1.address, "hxcc7b1f5fb98ca1eeaf9586bc08048814cb0d4d3d")

    def test1(self):
        """ Case the private key is not composed of 32 bytes.
        """
        try:
            wallet1 = Wallet.create_wallet_by_private_key('71fc378d3a3fb92b57474af156f9d277c9b60a923a1db75575b1cc')
        except TypeError:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()