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

from .general import has_keys


def validate_block(response_json: dict) -> bool:
    """Validate response from a block has right format.

    :param response_json. type(dict).
    :return: type(bool).
    """
    inner_key_name_of_block = ["version", "prev_block_hash", "merkle_tree_root_hash", "time_stamp",
                               "confirmed_transaction_list"]
    is_valid = response_json["result"]["response_code"] is 0 and has_keys(response_json["result"]["block"],
                                                                          inner_key_name_of_block)
    return is_valid


def validate_last_block(response_json: dict) -> bool:
    """Check the response json of the last block has right format.

    :param response_json. type(dict)
    :return: type(bool)
    """
    inner_key_name_of_result = ["response_code", "block"]
    inner_key_name_of_block = ["version", "prev_block_hash", "merkle_tree_root_hash", "time_stamp", \
                               "confirmed_transaction_list", "block_hash", "height", "peer_id", "signature"]

    is_valid = response_json["result"]["response_code"] is 0 and \
               has_keys(response_json["result"], inner_key_name_of_result) and \
               has_keys(response_json["result"]["block"], inner_key_name_of_block)
    return is_valid
