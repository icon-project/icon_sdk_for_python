from abc import *

# todo: 지원하는 메소드 범위 결정
# todo: 문서 배포 방식 결정 (readme.md or document)
# todo: structure 결정


class Wallet:

    @staticmethod
    def __generate_the_version_wallet_api(version: str, api_uri: str, wallet_info: dict, address: str,
                                          hex_public_key: str) -> object:
        """Generate a target version wallet api object and return it.

        :param version: a version of wallet api
        :param wallet_info: dictionary data of keystore file
        :param address: the address of
        :param hex_public_key: a public key in hexadecimal
        :return: an object of the version wallet api
        """
        _the_version_wallet_api = None  # type: object
        if version == "2.0":
            _the_version_wallet_api = WalletApiV2(api_uri, wallet_info, address, hex_public_key)
        elif version == "3.0":
            _the_version_wallet_api = WalletApiV3(api_uri, wallet_info, address, hex_public_key)
        return _the_version_wallet_api

    @classmethod
    def create_wallet_by_private_key(cls, version: str, api_uri: str, hex_private_key: str, password: str):
        """Create a wallet object by private key without keystore file.

        :param version: a version of wallet api
        :param api_uri: uri of target api
        :param hex_private_key: a private key in hexadecimals
        :return: an object of the version wallet api
        """
        # todo: procedure of create wallet object.
        hex_private_key = None
        return cls.__generate_the_version_wallet_api(version=version, api_uri=api_uri, wallet_info="default", address="default",
                                                     public_key="default")

    @classmethod
    def create_keystore_file_of_wallet(cls, version: str, api_uri: str, keystore_file_path: str, keystore_file_password: str):
        """Create a wallet object and keystore file on file path.

        :param version: a version of wallet api
        :param api_uri: uri of target api
        :param keystore_file_path: file path of keystore file
        :param keystore_file_password: password of keystore file
        :return: an object of the version wallet api
        """

        # todo: procedure of create wallet keystore file on the file path.
        # todo: procedure of create wallet object.
        return cls.__generate_the_version_wallet_api(version=version, api_uri=api_uri, wallet_info="default",
                                                     address="default", public_key="default")

    @classmethod
    def open_keystore_file_of_wallet(cls, version: str, api_uri: str, keystore_file_path, keystore_file_password):
        """Open a wallet being on keystore file path and return a wallet object.

        :param version: a version of wallet api
        :param api_uri: uri of target api
        :param keystore_file_path: file path of keystore file
        :param keystore_file_password: password of keystore file
        :return: an object of the version wallet api
        """

        # todo: procedure of open wallet keystore file on the file path.
        # todo: procedure of create wallet object.
        return cls.__generate_the_version_wallet_api(version=version, api_uri=api_uri, wallet_info="default",
                                                     address="default", public_key="default")


class AbstractWalletApi(metaclass=ABCMeta):
    """ Wallet API 메소드를 정의한 부모 클래스 """

    def __init__(self, api_uri: str, wallet_info: dict, address: str, hex_public_key: str):
        self.__api_uri = api_uri    # type: str
        self.__wallet_info = wallet_info    # type: dict
        self.__address = address    # type: str
        self.__public_key = hex_public_key  # type: str

    @property
    def api_uri(self):
        return self.__api_uri

    @property
    def wallet_info(self):
        return self.__wallet_info

    @property
    def address(self):
        return self.__address

    @property
    def public_key(self):
        return self.__public_key

    def __print_invalid_version(self):
        print("No support the api in the version")

    def get_wallet_info(self):
        """Get information of wallet.

        :return: Wallet information. type(dict).
        """
        self.__print_invalid_version()

    def get_address(self):
        self.__print_invalid_version()

    def get_private_key(self, password):
        self.__print_invalid_version()

    def transfer_value_by_private_key(self, hex_private_key: str, address_to: str, amount: str, fee: str):
        self.__print_invalid_version()

    def transfer_value(self, password: str, address_to: str, amount: str, fee: str):
        self.__print_invalid_version()

    def get_last_block(self):
        """Get information of the last block.

        :return: Response
        """
        self.__print_invalid_version()

    def get_block_by_height(self, height: str):
        """Get information of the block of that height.

        :param height: height of that block. type(int).
        :return: Response
        """
        self.__print_invalid_version()

    def get_block_by_hash(self, hash: str):
        """ Get information of the block of that hash.

        :param hash: hash value of the block which is used for ​​an digital signature. A string of 64 hexadecimal digits.
        :return: Response
        """
        self.__print_invalid_version()

    def icx_call(self, address_from, address_to, data_method, data_params):
        """Call an external method in SCORE.


        :param address_from: an address which send transaction
        :param address_to: an SCORE's address
        :param data_method: an external method of SCORE
        :param data_params: parameters of the external method
        :return: response
        """
        self.__print_invalid_version()

    def get_balance(self):
        """Get an balance from the address of SCORE or wallet.

        :return: Response
        """
        self.__print_invalid_version()

    def get_score_api(self, address_score):
        """Get information of SCORE's api methods.

        :param address_score: an address of SCORE
        :return: Response
        """
        self.__print_invalid_version()

    def get_total_supply(self):
        """Get total amount of coins currently issued
        :return: Response
        """
        self.___print_invalid_verion()

    def get_tx_result(self, hash):
        """Get result of transaction by that hash.

        :param hash: a hash value of transaction
        :return: Response
        """
        self.__print_invalid_version()

    def get_tx_by_hash(self):
        """Get information of transaction by hash.

        :return: Response
        """
        self.__print_invalid_version()


class WalletApiV2(AbstractWalletApi):
    """ V2에서 제공하는 Wallet API 메소드를 정의한 자식 클래스 """

    def get_private_key(self, password):
        pass

    def transfer_value_by_private_key(self, hex_private_key: str, to: str, amount: str, fee: str):
        pass

    def transfer_value(self, password: str, to: str, amount: str, fee: str):
        pass

    def get_wallet_info(self):
        print(super().api_uri)
        pass

    def get_balance(self):
        pass

    def get_address(self):
        pass

    def get_block_by_height(self, height: str):
        pass

    def get_block_by_hash(self, hash: str):
        pass

    def get_last_block(self):
        pass


class WalletApiV3(AbstractWalletApi):
    """ V3에서 제공하는 Wallet API 메소드를 정의한 자식 클래스 """

    def get_private_key(self, password):
        pass

    def transfer_value_by_private_key(self, hex_private_key: str, to: str, amount: str, fee: str):
        pass

    def transfer_value(self, password: str, to: str, amount: str, fee: str):
        pass

    def get_wallet_info(self):
        pass

    def get_balance(self):
        pass

    def get_address(self):
        pass

    def get_block_by_height(self, height: str):
        pass

    def get_block_by_hash(self, hash: str):
        pass

    def get_last_block(self):
        pass

    def get_total_supply(self):
        pass

    def get_score_api(self):
        pass

    def icx_call(self):
        pass

# v2
from icx.wallet import Wallet

Wallet2 = Wallet.create_wallet_keystore_file("file_path", "password")
Wallet2.get_wallet_info()
Wallet2.icx_call()

# v3
from icon.wallet import Wallet

Wallet3 = Wallet.create_wallet("3.0", "testnet", "private_key", "password")
Wallet3.get_wallet_info()


