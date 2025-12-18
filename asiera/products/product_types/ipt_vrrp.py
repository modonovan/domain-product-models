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

""" IP Transit VRRP service, for use by clients """

from typing import Annotated
from annotated_types import Len
from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SI, SubscriptionLifecycle
from pydantic import computed_field


from products.product_blocks.ipt_virtual_circuit import (
    IPTVirtualCircuitBlock,
    IPTVirtualCircuitBlockInactive,
    IPTVirtualCircuitBlockProvisioning,
)

from products.product_blocks.ipt_vrrp_config import (
    IPTVRRPConfig,
    IPTVRRPConfigInactive,
    IPTVRRPConfigProvisioning,
)

ListOfCircuits = Annotated[list[SI], Len(min_length=1, max_length=2)]


class IPTVRRPInactive(SubscriptionModel, is_base=True):
    """
    This is the base model for IPT VRRP services.
    """

    vrrp_config: IPTVRRPConfigInactive
    virtual_circuits: ListOfCircuits[IPTVirtualCircuitBlockInactive]

    @property
    def netbox_service_type(self) -> str:
        return "circuits/virtual_circuits"

    @property
    def circuit_a(self) -> IPTVirtualCircuitBlockInactive:
        return sorted(self.virtual_circuits, key=lambda x: str(x.ims_vc_id))[0]

    @property
    def circuit_b(self) -> IPTVirtualCircuitBlockInactive:
        return sorted(self.virtual_circuits, key=lambda x: str(x.ims_vc_id))[1]


class IPTVRRPProvisioning(IPTVRRPInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the IPT VRRP service.
    """

    vrrp_config: IPTVRRPConfigProvisioning
    virtual_circuits: ListOfCircuits[IPTVirtualCircuitBlockProvisioning]

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        Returns the title of the IPT VRRP service.
        """
        return "IPT VRRP Block"

    @property
    def circuit_a(self) -> IPTVirtualCircuitBlockProvisioning:
        return sorted(self.virtual_circuits, key=lambda x: str(x.ims_vc_id))[0]

    @property
    def circuit_b(self) -> IPTVirtualCircuitBlockProvisioning:
        return sorted(self.virtual_circuits, key=lambda x: str(x.ims_vc_id))[1]


class IPTVRRP(IPTVRRPProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the IPT VRRP service.
    """

    vrrp_config: IPTVRRPConfig
    virtual_circuits: ListOfCircuits[IPTVirtualCircuitBlock]

    @property
    def circuit_a(self) -> IPTVirtualCircuitBlock:
        return sorted(self.virtual_circuits, key=lambda x: str(x.ims_vc_id))[0]

    @property
    def circuit_b(self) -> IPTVirtualCircuitBlock:
        return sorted(self.virtual_circuits, key=lambda x: str(x.ims_vc_id))[1]
