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

""" Core Link SAP, representing a virtual interface. Used by Core Links """

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field

from products.product_blocks.core_port import (
    CorePortBlock,
    CorePortBlockInactive,
    CorePortBlockProvisioning,
)
from products.product_blocks.core_lag_port import (
    CoreLAGPortBlock,
    CoreLAGPortBlockInactive,
    CoreLAGPortBlockProvisioning,
)


class CoreSAPBlockInactive(ProductBlockModel, product_block_name="CoreSAP"):
    """
    This is the inactive version of the Core SAP product block.
    """

    port: CorePortBlockInactive | CoreLAGPortBlockInactive | None = None
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    unit_id: int | None = None
    freetext: str | None = None
    media_type: str | None = None


class CoreSAPBlockProvisioning(CoreSAPBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning version of the Core SAP product block.
    It represents a Core SAP that is in the process of being provisioned.
    We like to think of it as being "almost there" but not yet fully active. In this state, all required fields should be populated to facilitate successful provisioning.
    """

    port: CorePortBlockProvisioning | CoreLAGPortBlockProvisioning
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    unit_id: int | None = None
    freetext: str | None = None
    media_type: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        The title of the Core SAP product block.
        """
        return f"Core SAP on port {self.port.port_name} on {self.port.node.node_name}"


class CoreSAPBlock(CoreSAPBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active version of the Core SAP product block.
    It represents a Core SAP that is fully provisioned and active.
    In this state, all required fields must be populated, and the Core SAP is operational within the ASIERA service.
    """

    port: CorePortBlock | CoreLAGPortBlock
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    unit_id: int
    freetext: str | None = None
    media_type: str
