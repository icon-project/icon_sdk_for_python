class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class PasswordIsNotAcceptable(Error):
    """Exception raised for "Password is wrong"."""
    pass


class FilePathIsWrong(Error):
    """Exception raised for "File path is wrong". """
    pass


class FileExists(Error):
    """Exception raised for "File path is wrong". """
    pass


class NoPermissionToWriteFile(Error):
    """Exception raised for "No permission to write file". """
    pass


class NonExistKey(Error):
    """Exception raised for "Dictionary has not key." """
    pass


class PasswordIsWrong(Error):
    """Exception raised for "Password is incorrect." """
    pass


class AddressIsWrong(Error):
    """Exception raised for "Wallet address is invalid." """
    pass


class NotEnoughBalanceInWallet(Error):
    """Exception raised for "Wallet does not have enough balance." """
    pass


class AmountIsInvalid(Error):
    """Exception raised for "Amount is Invalid." """
    pass


class TransferFeeIsInvalid(Error):
    """Exception raised for "Transfer Fee is Invalid." """
    pass


class FilePathWithoutFileName(Error):
    """Exception raised for "File Path without a file name." """
    pass


class FeeIsBiggerThanAmount(Error):
    """Exception raised for "Fee is bigger than Amount" """
    pass


class NotAKeyStoreFile(Error):
    """Exception raised for 'Not a Key Store File.' """
    pass


class AddressIsSame(Error):
    """Exception raised for 'Wallet address to transfer is same as Wallet address to deposit.' """
    pass
