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

""" IP Transit Static service, for use by clients """

from typing import Annotated
from annotated_types import Len
from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SI, SubscriptionLifecycle

from products.product_blocks.ipt_virtual_circuit import (
    IPTVirtualCircuitBlock,
    IPTVirtualCircuitBlockInactive,
    IPTVirtualCircuitBlockProvisioning,
)

from products.product_blocks.static_route import (
    StaticRouteBlock,
    StaticRouteBlockInactive,
    StaticRouteBlockProvisioning,
)

ListOfStaticRoutes = Annotated[list[SI], Len(min_length=0)]


class IPTStaticInactive(SubscriptionModel, is_base=True):
    """
    This is the base class for the IP Transit Static service.
    """

    virtual_circuit: IPTVirtualCircuitBlockInactive
    # static_route_list
    static_routes: ListOfStaticRoutes[StaticRouteBlockInactive]

    @property
    def netbox_service_type(self) -> str:
        return "circuits/virtual_circuits"


class IPTStaticProvisioning(IPTStaticInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning class for the IP Transit Static service.
    """

    virtual_circuit: IPTVirtualCircuitBlockProvisioning
    static_routes: ListOfStaticRoutes[StaticRouteBlockProvisioning]


class IPTStatic(IPTStaticProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the IP Transit Static service.
    """

    virtual_circuit: IPTVirtualCircuitBlock
    static_routes: ListOfStaticRoutes[StaticRouteBlock]
