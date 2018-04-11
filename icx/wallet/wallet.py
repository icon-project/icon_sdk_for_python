import json
import os
import codecs
from icx.custom_error import PasswordIsNotAcceptable, FileExists, NoPermissionToWriteFile, FilePathIsWrong, \
    FilePathWithoutFileName
from icx.utils import validate_password, get_timestamp_us, get_tx_hash, sign, create_jsonrpc_request_content, post, \
        get_payload_of_json_rpc_get_balance
from icx.signer import IcxSigner
from eth_keyfile import create_keyfile_json, extract_key_from_keyfile


class Wallet:

    def __init__(self, wallet_data=None, public_key=None, api_url="https://testwallet.icon.foundation/api/", address=None):
        self.__wallet_info = json.loads(wallet_data) if wallet_data else wallet_data
        self.__address = self.__wallet_info["address"] if wallet_data else address          # an address of the wallet
        self.__public_key = public_key                                                      # a public key of the wallet
        self.__api_url = api_url                                                            # a target url for api

    @property
    def address(self):
        return self.__address

    @property
    def wallet_info(self):
        return self.__wallet_info

    @property
    def public_key(self):
        return self.__public_key

    @property
    def api_url(self):
        return self.__api_url

    @address.setter
    def address(self, address):
        self.__address = address

    @wallet_info.setter
    def wallet_info(self, wallet_info):
        self.__wallet_info = wallet_info

    @public_key.setter
    def public_key(self, public_key):
        self.__public_key = public_key

    @api_url.setter
    def api_url(self, api_url):
        self.__api_url = api_url

    @staticmethod
    def create_keystore_file_of_wallet(keystore_file_path, password):
        """ create both a wallet and a keystore file

           :param keystore_file_path: File path for the keystore file of the wallet.
           :param password:  Password including alphabet character, number, and special character.
           If the user doesn't give password with -p, then CLI will show the prompt and user need to type the password.
           :return: Instance of Wallet class.
           """

        if not validate_password(password):
            raise PasswordIsNotAcceptable

        try:
            signer = IcxSigner()
            byte_private_key = signer.private_key_bytes
            byte_public_key = signer.public_key_bytes

            key_store_contents = create_keyfile_json(byte_private_key, bytes(password, 'utf-8'), iterations=262144)
            key_store_contents['address'] = "hx" + signer.address.hex()
            key_store_contents['coinType'] = 'icx'
            json_string = json.dumps(key_store_contents)

            store_wallet(keystore_file_path, json_string)

            text = f'Address({len(signer.address)}): hx{signer.address.hex()}\n' \
                   + f'PrivateKey({len(byte_private_key)}): 0x{byte_private_key.hex()}\n' \
                   + f'PublicKey({len(byte_public_key)}): 0x{byte_public_key.hex()}'

            w = Wallet(json_string)
            print(text)
            return w

        except FileExistsError:
            raise FileExists
        except PermissionError:
            raise NoPermissionToWriteFile
        except FileNotFoundError:
            raise FilePathIsWrong
        except IsADirectoryError:
            raise FilePathWithoutFileName

    @staticmethod
    def create_wallet_by_private_key(hex_private_key=None):
        """ create wallet without keystore file

           :param hex_private_key: the private key with a hexadecimal number
           :return: Instance of Wallet class.
           """

        byte_private_key, is_byte = None, None

        if hex_private_key:
            byte_private_key = bytes.fromhex(hex_private_key)
            is_byte = True

        try:

            signer = IcxSigner(byte_private_key, is_byte)
            byte_private_key = signer.private_key_bytes
            byte_public_key = signer.public_key_bytes

            w = Wallet()
            w.address = "hx" + signer.address.hex()

            text = f'Address({len(signer.address)}): hx{signer.address.hex()}\n' \
                   + f'PrivateKey({len(byte_private_key)}): 0x{byte_private_key.hex()}\n' \
                   + f'PublicKey({len(byte_public_key)}): 0x{byte_public_key.hex()}'

            print(text)
            return w

        except TypeError:
            raise TypeError

    def open_keystore_file(self, keystore_file_path, password):
        """ open the keystore file and read the information of the file """

        return "keystore_info"

    def transfer(self, private_key, url, from_address, to_address, loop, fee):
        """ transfer the specific value with private key """

        pass

    def get_wallet_info(self):
        """ get the keystore file information and the balance """

        pass

    def get_balance(self):
        """ get the balance """

        pass

    def get_address(self):
        """ get the address"""

        pass


def make_params(user_address, to, amount, fee, method, private_key_bytes):
    """Make params for jsonrpc format.

    :param user_address: Address of user's wallet.
    :param to: Address of wallet to receive the asset.
    :param amount: Amount of money.
    :param fee: Transaction fee.
    :param method: Method type. type(str)
    :param private_key_bytes: Private key of user's wallet.
    :return:
    type(dict)
    """
    params = {
        'from': user_address,
        'to': to,
        'value': hex(amount),
        'fee': hex(fee),
        'timestamp': str(get_timestamp_us())
    }
    tx_hash_bytes = get_tx_hash(method, params)
    signature_bytes = sign(private_key_bytes, tx_hash_bytes)
    params['tx_hash'] = tx_hash_bytes.hex()
    params['signature'] = signature_bytes.decode()

    return params


def store_wallet(file_path, json_string):
    """ Store wallet information file in JSON format.

    :param file_path: The path where the file will be saved. type: str
    :param json_string: Contents of key_store_file
    """
    if os.path.isfile(file_path):
        raise FileExistsError

    with open(file_path, 'wt') as f:
        f.write(json_string)


def make_key_store_content(password):
    """ Make a content of key_store.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn't give password with -p, then CLI will show the prompt and user need to type the password.
    :return:
    key_store_content(dict)
    """
    signer = IcxSigner()
    private_key = signer.private_key
    key_store_contents = create_keyfile_json(private_key, bytes(password, 'utf-8'), iterations=262144)
    icx_address = "hx" + signer.address.hex()
    key_store_contents['address'] = icx_address
    key_store_contents['coinType'] = 'icx'
    return key_store_contents


def key_from_key_store(file_path, password):
    """

    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as file:
        private_key = extract_key_from_keyfile(file, password)
    return private_key


def get_balance(address, url):
    """ Get balance of the address indicated by address.

    :param address: icx account address starting with 'hx'
    :param url:
    :return: icx
    """
    url = f'{url}v2'

    method = 'icx_getBalance'
    params = {'address': address}
    payload = create_jsonrpc_request_content(0, method, params)
    response = post(url, payload)
    content = response.json()
    hex_balance = content['result']['response']
    dec_loop_balance = int(hex_balance, 16)

    return dec_loop_balance


def read_wallet(file_path):
    """Read keystore file

    :param file_path:
    :return: wallet_info
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError
    with codecs.open(file_path, 'r', 'utf-8-sig') as f:
        wallet_info = json.load(f)
        f.close()

    return wallet_info


def get_balance_after_trasfer(address, url, request_gen):
    """ Get balance of the address indicated by address for check balance before transfer icx.

    :param address: Icx account address starting with 'hx'
    :param url: Api url. type(str)
    :param request_gen:
    :return: Balance of the user's wallet.
    """
    payload_for_balance = get_payload_of_json_rpc_get_balance(address, url)

    next(request_gen)
    balance_content = request_gen.send(payload_for_balance).json()

    balance = balance_content['result']['response']
    balance_loop = int(balance, 16)
    return balance_loop
