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

""" L3VPN SAP, representing a virtual interface. """

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field

from products.product_blocks.port import (
    PortBlock,
    PortBlockInactive,
    PortBlockProvisioning,
)
from products.product_blocks.lag_port import (
    LAGPortBlock,
    LAGPortBlockInactive,
    LAGPortBlockProvisioning,
)


class SAPL3VPNBlockInactive(ProductBlockModel, product_block_name="SAPL3VPN"):
    """
    #TODO fill me in
    """

    port: PortBlockInactive | LAGPortBlockInactive | None = None
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    mtu: int | None = None
    ipv4_prefix_ids: list[int] | None = None
    ipv6_prefix_ids: list[int] | None = None
    unit_id: int | None = None
    vlan: int | None = None
    route_distinguisher: str | None = None
    # hub or spoke
    role: str | None = None
    # routing - BGP / Static
    routing: str | None = None
    # vrf route targets
    import_target: str | None = None
    export_target: str | None = None
    # BGP
    bgp_peer_as: str | None = None
    bgp_auth_key: str | None = None
    bgp_policy: str | None = None
    bgp_neighbour_ipv4_ipam_id: int | None = None
    bgp_neighbour_ipv6_ipam_id: int | None = None
    # VRRP / static
    vrrp_group: str | None = None
    vrrp_vip_ipv4_addr_id: int | None = None
    vrrp_priority: str | None = None


class SAPL3VPNBlockProvisioning(SAPL3VPNBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    port: PortBlockProvisioning | LAGPortBlockProvisioning
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    mtu: int
    ipv4_prefix_ids: list[int] | None = None
    ipv6_prefix_ids: list[int] | None = None
    unit_id: int
    vlan: int | None = None
    route_distinguisher: str | None = None
    role: str | None = None
    routing: str | None = None
    import_target: str | None = None
    export_target: str | None = None
    bgp_peer_as: str | None = None
    bgp_auth_key: str | None = None
    bgp_policy: str | None = None
    bgp_neighbour_ipv4_ipam_id: int | None = None
    bgp_neighbour_ipv6_ipam_id: int | None = None
    vrrp_group: str | None = None
    vrrp_vip_ipv4_addr_id: int | None = None
    vrrp_priority: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        #TODO fill me in
        """
        # return "L3VPN SAP Block"
        return f"Port {self.port.port_name} on {self.port.node.node_name}"


class SAPL3VPNBlock(SAPL3VPNBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    port: PortBlock | LAGPortBlock
    ipv4_ipam_id: int
    ipv6_ipam_id: int | None = None
    mtu: int
    ipv4_prefix_ids: list[int] | None = None
    ipv6_prefix_ids: list[int] | None = None
    unit_id: int
    vlan: int
    route_distinguisher: str
    role: str
    routing: str | None = None
    import_target: str | None = None
    export_target: str | None = None
    bgp_peer_as: str | None = None
    bgp_auth_key: str | None = None
    bgp_policy: str | None = None
    bgp_neighbour_ipv4_ipam_id: int | None = None
    bgp_neighbour_ipv6_ipam_id: int | None = None
    vrrp_group: str | None = None
    vrrp_vip_ipv4_addr_id: int | None = None
    vrrp_priority: str | None = None
