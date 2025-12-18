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
    #TODO fill me in
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
    #TODO fill me in
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
        #TODO fill me in
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
    #TODO fill me in
    """

    saps: ListOfSaps[SAPPPBlock]
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    ims_id: int
    speed: int
    speed_policer: bool
    vc_id: int
