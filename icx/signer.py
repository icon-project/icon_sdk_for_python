import hashlib
from secp256k1 import PrivateKey


class IcxSigner(object):
    """ ICX Signature utility class.
    """

    def __init__(self, data: object = None, raw: object = None) -> object:
        """
        :param data bytes or der (object):
        :param raw: (bool) True(bytes) False(der)
        """
        self.__private_key = PrivateKey(data, raw)

    @property
    def private_key_bytes(self):
        return self.__private_key.private_key

    @private_key_bytes.setter
    def private_key(self, data):
        self.__private_key.set_raw_privkey(data)

    @property
    def public_key_bytes(self):
        return self.__private_key.pubkey.serialize(compressed=False)

    @property
    def address(self):
        public_key_bytes = self.public_key_bytes
        return hashlib.sha3_256(public_key_bytes[1:]).digest()[-20:]

    def sign(self, msg_hash):
        """Make a signature using the hash value of msg.

        :param msg_hash: Result of sha3_256(msg) type(bytes)
        :return:
        Signature. type(bytes)
        """
        private_key_object = self.__private_key
        signature = private_key_object.ecdsa_sign(msg_hash, raw=True)
        return private_key_object.ecdsa_serialize(signature)

    def sign_recoverable(self, msg_hash):
        """Make a recoverable signature using message hash data.
        We can extract public key from recoverable signature.

        :param msg_hash: Hash data of message. type(bytes)
        :return:
        type(tuple)
        type(bytes): 65 bytes data , type(int): recovery id
        """
        private_key_object = self.__private_key
        recoverable_signature = private_key_object.ecdsa_sign_recoverable(msg_hash, raw=True)
        return private_key_object.ecdsa_recoverable_serialize(recoverable_signature)

    @staticmethod
    def from_bytes(data):
        return IcxSigner(data, raw=True)

    @staticmethod
    def from_der(data):
        return IcxSigner(data, raw=False)