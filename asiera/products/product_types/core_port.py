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

""" Interface subscription, representing a physical port. Only used by ASIERA. """

from enum import IntEnum

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from products.product_blocks.core_port import (
    CorePortBlock,
    CorePortBlockInactive,
    CorePortBlockProvisioning,
)

class CorePortSpeed(IntEnum):
    """
    Speed of physical port in Mbit/s.
    """

    _1000 = 1000
    _10000 = 10000
    _40000 = 40000
    _100000 = 100000
    _400000 = 400000

class CorePortInactive(SubscriptionModel, is_base=True):
    """
    This is the inactive state of the Core Port subscription.
    """

    speed: CorePortSpeed
    port: CorePortBlockInactive


class CorePortProvisioning(CorePortInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the Core Port subscription.
    """

    speed: CorePortSpeed
    port: CorePortBlockProvisioning


class CorePort(CorePortProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the Core Port subscription.
    """

    speed: CorePortSpeed
    port: CorePortBlock
