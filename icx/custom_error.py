#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 theloop Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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
