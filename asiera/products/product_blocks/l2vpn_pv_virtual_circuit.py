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

""" L2VPN virtual circuit, used by L2VPN Port-to-VLAN """

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
from products.product_blocks.sap_vv import (
    SAPVVBlock,
    SAPVVBlockInactive,
    SAPVVBlockProvisioning,
)

ListOfSaps = Annotated[list[SI], Len(min_length=2, max_length=2)]


class L2vpnPVVirtualCircuitBlockInactive(
    ProductBlockModel, product_block_name="L2vpnPVVirtualCircuit"
):
    """
    This block represents a L2VPN Port-to-VLAN virtual circuit in inactive state.
    """

    sap_p: SAPPPBlockInactive
    sap_v: SAPVVBlockInactive
    ims_id: int | None = None
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    speed: int | None = None
    speed_policer: bool | None = None
    vc_id: int | None = None


class L2vpnPVVirtualCircuitBlockProvisioning(
    L2vpnPVVirtualCircuitBlockInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This block represents a L2VPN Port-to-VLAN virtual circuit in provisioning state.
    """

    sap_p: SAPPPBlockProvisioning
    sap_v: SAPVVBlockProvisioning
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
        Title of the L2VPN PV virtual circuit block.
        """
        return (
            f"{self.speed} Mbit/s PV circuit between "
            f"{self.sap_p.port.node.node_name} and "
            f"{self.sap_v.port.node.node_name}"
        )


class L2vpnPVVirtualCircuitBlock(
    L2vpnPVVirtualCircuitBlockProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This block represents a L2VPN Port-to-VLAN virtual circuit in active state.
    """

    sap_p: SAPPPBlock
    sap_v: SAPVVBlock
    ims_id: int
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    speed: int
    speed_policer: bool
    vc_id: int
