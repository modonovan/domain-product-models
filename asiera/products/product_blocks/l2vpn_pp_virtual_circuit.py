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

""" L2VPN virtual circuit, used by L2VPN Port-to-Port """

from typing import Annotated

from annotated_types import Len
from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SI, SubscriptionLifecycle
from pydantic import computed_field

from products.product_blocks.sap_pp import (
    SAPPPBlock,
    SAPPPBlockInactive,
    SAPPPBlockProvisioning,
)

ListOfSaps = Annotated[list[SI], Len(min_length=2, max_length=2)]


class L2vpnPPVirtualCircuitBlockInactive(
    ProductBlockModel, product_block_name="L2vpnPPVirtualCircuit"
):
    """
    This block represents a L2VPN Port-to-Port virtual circuit in inactive state.
    2 SAPPPBlocks should be linked to this block to create a full Port-to-Port
    connection.
    1 SAPPPBlock represents 1 end of the Port-to-Port connection.
    2 SAPPPBlocks are required to create a full Port-to-Port connection.
    1 SAPPPBlock is linked to 1 port on a node.
    2 SAPPPBlocks linked to this block should be linked to ports on different nodes.
    1 SAPPPBlock is linked to 1 subscription.
    2 SAPPPBlocks linked to this block should be linked to different subscriptions.
    1 SAPPPBlock is linked to 1 customer.
    2 SAPPPBlocks linked to this block should be linked to the same customer.
    1 SAPPPBlock is linked to 1 product.
    2 SAPPPBlocks linked to this block should be linked to the same product.
    1 SAPPPBlock is linked to 1 virtual circuit.
    2 SAPPPBlocks linked to this block should be linked to the same virtual circuit.
    1 SAPPPBlock is linked to 1 speed.
    2 SAPPPBlocks linked to this block should be linked to the same speed.
    1 SAPPPBlock is linked to 1 speed policer. (we don't enforce this yet)
    2 SAPPPBlocks linked to this block should be linked to the same speed policer.
    1 SAPPPBlock is linked to 1 IMS ID. (we don't enforce this yet)
    2 SAPPPBlocks linked to this block should be linked to the same IMS ID.
    1 SAPPPBlock is linked to 1 IMS VC ID. (we don't enforce this yet)
    2 SAPPPBlocks linked to this block should be linked to the same IMS VC ID.
    1 SAPPPBlock is linked to 1 lifecycle state.
    2 SAPPPBlocks linked to this block should be linked to the same lifecycle state.
    1 SAPPPBlock is linked to 1 product block.
    2 SAPPPBlocks linked to this block should be linked to the same product block.
    1 SAPPPBlock is linked to 1 product block name.
    2 SAPPPBlocks linked to this block should be linked to the same product block name.
    1 SAPPPBlock is linked to 1 product block model.
    2 SAPPPBlocks linked to this block should be linked to the same product block model.
    1 SAPPPBlock is linked to 1 product block type.
    2 SAPPPBlocks linked to this block should be linked to the same product block type.
    1 SAPPPBlock is linked to 1 product block version.
    2 SAPPPBlocks linked to this block should be linked to the same product block version.
    1 SAPPPBlock is linked to 1 product block description.
    2 SAPPPBlocks linked to this block should be linked to the same product block description.
    1 SAPPPBlock is linked to 1 product block metadata.
    2 SAPPPBlocks linked to this block should be linked to the same product block metadata.
    1 SAPPPBlock is linked to 1 product block created at.
    2 SAPPPBlocks linked to this block should be linked to the same product block created at.
    1 SAPPPBlock is linked to 1 product block updated at.
    2 SAPPPBlocks linked to this block should be linked to the same product block updated at.
    1 SAPPPBlock is linked to 1 product block deleted at.
    2 SAPPPBlocks linked to this block should be linked to the same product block deleted at.
    1 SAPPPBlock is linked to 1 product block extra attributes.
    2 SAPPPBlocks linked to this block should be linked to the same product block extra attributes.
    1 SAPPPBlock is linked to 1 product block tags.
    2 SAPPPBlocks linked to this block should be linked to the same product block tags
    """

    saps: ListOfSaps[SAPPPBlockInactive]
    ims_id: int | None = None
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    speed: int | None = None
    speed_policer: bool | None = None
    vc_id: int | None = None


class L2vpnPPVirtualCircuitBlockProvisioning(
    L2vpnPPVirtualCircuitBlockInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This block represents a L2VPN Port-to-Port virtual circuit in provisioning state.
    """

    saps: ListOfSaps[SAPPPBlockProvisioning]
    ims_id: int | None = None
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    speed: int
    speed_policer: bool
    vc_id: int

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        Returns a human-readable title for the virtual circuit.
        """
        return (
            f"{self.speed} Mbit/s PP circuit between "
            f"{self.saps[0].port.node.node_name} and "
            f"{self.saps[1].port.node.node_name}"
        )

    @property
    def sap_a(self) -> SAPPPBlockProvisioning:
        return sorted(self.saps, key=lambda x: str(x.ims_id))[0]

    @property
    def sap_b(self) -> SAPPPBlockProvisioning:
        return sorted(self.saps, key=lambda x: str(x.ims_id))[1]


class L2vpnPPVirtualCircuitBlock(
    L2vpnPPVirtualCircuitBlockProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This block represents a L2VPN Port-to-Port virtual circuit in active state.
    """

    saps: ListOfSaps[SAPPPBlock]
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    ims_id: int
    speed: int
    speed_policer: bool
    vc_id: int
