# Copyright 2019-2023 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Across various product blocks, certain enumerations are shared. This module contains those shared enumerations."""

from enum import Enum


class EnumBase(str, Enum):
    """
    This is a base class or function for enumerations that inherit from both `str` and `Enum`.
    It provides a method to list all the values of the enumeration members.
    """

    @classmethod
    def list(cls):
        return [member.value for member in cls]


class NodeStatus(EnumBase):
    """
    This function explicitly defines the operational status of a node. Your IMS of choice may have predefined statues.
    In our instance, we use NetBox, which has its own set of statuses. This enumeration serves to standardize the statuses we use across our application,
    ensuring consistency regardless of the underlying IMS.
    """

    """Operational status of a node."""

    OFFLINE = "offline"
    ACTIVE = "active"
    PLANNED = "planned"
    STAGED = "staged"
    FAILED = "failed"
    INVENTORY = "inventory"
    DECOMMISSIONING = "decommissioning"
