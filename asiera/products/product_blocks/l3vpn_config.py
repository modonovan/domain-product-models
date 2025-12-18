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

""" IP Transit VRRP config, used by IPT VRRP """

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field


class L3VPNConfigInactive(ProductBlockModel, product_block_name="L3VPNConfig"):
    """
    #TODO fill me in
    """

    l3vpn_name: str | None = None
    l3vpn_instance: str | None = None
    vrf_id: int | None = None
    route_distinguisher: str | None = None
    # ID for Netbox plugins/bgp/community
    hub_route_target_id: int | None = None
    spoke_route_target_id: int | None = None


class L3VPNConfigProvisioning(
    L3VPNConfigInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    #TODO fill me in
    """

    l3vpn_name: str | None = None
    l3vpn_instance: str | None = None
    vrf_id: int | None = None
    route_distinguisher: str | None = None
    hub_route_target_id: int | None = None
    spoke_route_target_id: int | None = None



    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        #TODO fill me in
        """
        return "L3VPN Config Block"


class L3VPNConfig(
    L3VPNConfigProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    #TODO fill me in
    """

    l3vpn_name: str
    l3vpn_instance: str
    vrf_id: int
    route_distinguisher: str
    hub_route_target_id: int
    spoke_route_target_id: int