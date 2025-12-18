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

""" Core link subscription. Only used by HEAnet """


from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from products.product_blocks.core_virtual_circuit import (
    CoreVirtualCircuitBlock,
    CoreVirtualCircuitBlockInactive,
    CoreVirtualCircuitBlockProvisioning,
)


class CoreLinkInactive(SubscriptionModel, is_base=True):
    """
    #TODO fill me in
    """

    virtual_circuit: CoreVirtualCircuitBlockInactive

    @property
    def netbox_service_type(self) -> str:
        return "circuits/virtual_circuits"


class CoreLinkProvisioning(CoreLinkInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    virtual_circuit: CoreVirtualCircuitBlockProvisioning


class CoreLink(CoreLinkProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    virtual_circuit: CoreVirtualCircuitBlock
