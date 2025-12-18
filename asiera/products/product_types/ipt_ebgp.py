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

""" IP Transit eBGP service, for use by clients """

from typing import Annotated
from annotated_types import Len
from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SI, SubscriptionLifecycle

from products.product_blocks.bgp_route import (
    BgpRouteBlock,
    BgpRouteBlockInactive,
    BgpRouteBlockProvisioning,
)

from products.product_blocks.ipt_virtual_circuit import (
    IPTVirtualCircuitBlock,
    IPTVirtualCircuitBlockInactive,
    IPTVirtualCircuitBlockProvisioning,
)

ListOfBgpRoutes = Annotated[list[SI], Len(min_length=1)]


class IPTeBGPInactive(SubscriptionModel, is_base=True):
    """
    #TODO fill me in
    """

    virtual_circuit: IPTVirtualCircuitBlockInactive
    bgp_routes: ListOfBgpRoutes[BgpRouteBlockInactive]

    @property
    def netbox_service_type(self) -> str:
        return "circuits/virtual_circuits"


class IPTeBGPProvisioning(IPTeBGPInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    virtual_circuit: IPTVirtualCircuitBlockProvisioning
    bgp_routes: ListOfBgpRoutes[BgpRouteBlockProvisioning]


class IPTeBGP(IPTeBGPProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    virtual_circuit: IPTVirtualCircuitBlock
    bgp_routes: ListOfBgpRoutes[BgpRouteBlock]
