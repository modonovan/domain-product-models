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

""" L2VPN virtual circuit, used by L2VPN VLAN-to-VLAN with Translation """

from typing import Annotated

from annotated_types import Len
from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SI, SubscriptionLifecycle
from pydantic import computed_field

from products.product_blocks.sap_vv import (
    SAPVVBlock,
    SAPVVBlockInactive,
    SAPVVBlockProvisioning,
)

ListOfSaps = Annotated[list[SI], Len(min_length=2, max_length=2)]


class L2vpnVVTranslationVirtualCircuitBlockInactive(
    ProductBlockModel, product_block_name="L2vpnVVTranslationVirtualCircuit"
):
    """
    #TODO fill me in
    """

    sap_a: SAPVVBlockInactive
    sap_b: SAPVVBlockInactive
    ims_id: int | None = None
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    speed: int | None = None
    speed_policer: bool | None = None
    vc_id: int | None = None


class L2vpnVVTranslationVirtualCircuitBlockProvisioning(
    L2vpnVVTranslationVirtualCircuitBlockInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    #TODO fill me in
    """

    sap_a: SAPVVBlockProvisioning
    sap_b: SAPVVBlockProvisioning
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
            f"{self.speed} Mbit/s VV with translation circuit between "
            f"{self.sap_a.port.node.node_name} and "
            f"{self.sap_b.port.node.node_name}"
        )


class L2vpnVVTranslationVirtualCircuitBlock(
    L2vpnVVTranslationVirtualCircuitBlockProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    #TODO fill me in
    """

    sap_a: SAPVVBlock
    sap_b: SAPVVBlock
    ims_id: int
    # reference to Netbox virtual circuit object
    ims_vc_id: int | None = None
    speed: int
    speed_policer: bool
    vc_id: int
