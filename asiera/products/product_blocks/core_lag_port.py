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
LAG Port, used by LAG Port product and SAP product blocks
On each LAG port lives a collection of member ports or SAPs.
The SAPs have their own product block, but the member ports are just references to Core Port product blocks.
"""

from typing import List

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field

from products.product_blocks.node import (
    NodeBlock,
    NodeBlockInactive,
    NodeBlockProvisioning,
)


class CoreLAGPortBlockInactive(ProductBlockModel, product_block_name="CoreLAGPort"):
    """
    This is the inactive version of the Core LAG Port product block.
    """

    port_name: str | None = None
    port_type: str | None = None
    port_description: str | None = None
    port_mode: str | None = None
    auto_negotiation: bool | None = None
    lldp: bool | None = None
    enabled: bool | None = None
    node: NodeBlockInactive | None = None
    ims_id: int | None = None
    mgmt_only: bool | None = None


class CoreLAGPortBlockProvisioning(CoreLAGPortBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning version of the Core LAG Port product block.
    """

    port_name: str
    port_type: str
    port_description: str | None = None
    port_mode: str
    auto_negotiation: bool
    lldp: bool
    enabled: bool
    node: NodeBlockProvisioning
    ims_id: int
    mgmt_only: bool


    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        The title of the Core LAG Port product block.
        """
        return f"Core LAG port {self.port_name} on {self.node.node_name}"


class CoreLAGPortBlock(CoreLAGPortBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active version of the Core LAG Port product block.
    It represents a Core LAG Port that is fully provisioned and active.
    In this state, all required fields must be populated, and the Core LAG Port is operational within the ASIERA service.
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
