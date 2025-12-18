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

"""
Port, used by Port product and SAP product blocks
"""

from typing import List

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle, strEnum
from pydantic import computed_field

from products.product_blocks.node import (
    NodeBlock,
    NodeBlockInactive,
    NodeBlockProvisioning,
)


class CorePortMode(strEnum):
    """
    Valid port modes
    """

    TAGGED = "tagged"
    ACCESS = "access"


class CorePortBlockInactive(ProductBlockModel, product_block_name="Port"):
    """
    This is the inactive version of the Core Port product block.
    """

    port_name: str | None = None
    port_type: str | None = None
    port_description: str | None = None
    port_mode: str | None = None
    auto_negotiation: bool | None = None
    lldp: bool | None = None
    enabled: bool | None = None
    node: NodeBlockInactive | NodeBlockProvisioning | NodeBlock | None = None
    ims_id: int | None = None
    mgmt_only: bool | None = None


class CorePortBlockProvisioning(CorePortBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning version of the Core Port product block. This
    represents a Core Port that is in the process of being provisioned.
    We like to think of it as being "almost there" but not yet fully active. In this state, all required fields should be populated to facilitate successful provisioning.
    """

    port_name: str
    port_type: str
    port_description: str | None = None
    port_mode: str
    auto_negotiation: bool
    lldp: bool
    enabled: bool
    node: NodeBlockProvisioning | NodeBlock
    ims_id: int
    mgmt_only: bool

    def _active_sap_blocks(self) -> List:
        """
        Tie back to active SAP blocks using this port
        """
        from products.product_blocks.sap import SAPBlock

        return [
            SAPBlock.from_db(subscription_instance.subscription_instance_id)
            for subscription_instance in self.in_use_by
            if subscription_instance.product_block.tag == "CoreSAP"
            and subscription_instance.subscription.status == SubscriptionLifecycle.ACTIVE
        ]

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        The title of the Core Port product block.
        """
        return f"Core port {self.port_name} on {self.node.node_name}"


class CorePortBlock(CorePortBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active version of the Core Port product block.
    It represents a Core Port that is fully provisioned and active.
    In this state, all required fields must be populated, and the Core Port is operational within the ASIERA service.
    """

    port_name: str
    port_type: str
    port_description: str | None = None
    port_mode: str
    auto_negotiation: bool
    lldp: bool
    enabled: bool
    node: NodeBlock
    ims_id: int
    mgmt_only: bool
