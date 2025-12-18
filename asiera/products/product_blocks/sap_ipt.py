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

""" IP Transit SAP, representing a virtual interface. Used by IPT Virtual Circuit """

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field
from services.netbox import get_ip_address

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


class SAPIPTBlockInactive(ProductBlockModel, product_block_name="SAPIPT"):
    """
    This is the inactive state of the IPT SAP Block
    """

    port: PortBlockInactive | LAGPortBlockInactive | None = None
    mtu: int | None = None
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    unit_id: int | None = None
    vlan: int | None = None


class SAPIPTBlockProvisioning(SAPIPTBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the IPT SAP Block
    """

    port: PortBlockProvisioning | LAGPortBlockProvisioning
    mtu: int
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    unit_id: int
    vlan: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        Returns a human-readable title for the IPT SAP block.
        """
        # return "IPT SAP Block"
        return f"Port {self.port.port_name} on {self.port.node.node_name}"

    @computed_field  # type: ignore[misc]
    @property
    def ipv6_linklocal_addr(self) -> str:
        """
        This generates a link local v6 address from ipv6_ipam_id. This is needed for VRRP.
        """
        # example if v6 addr is 2001:770:50::4/64
        # should return fe80::770:50:4/64
        if self.ipv6_ipam_id:
            v6_addr = str(get_ip_address(id=self.ipv6_ipam_id))
            return (v6_addr.replace("::", ":")).replace("2001:", "fe80::")
        return None


class SAPIPTBlock(SAPIPTBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the IPT SAP Block
    """

    port: PortBlock | LAGPortBlock
    mtu: int
    ipv4_ipam_id: int | None = None
    ipv6_ipam_id: int | None = None
    unit_id: int
    vlan: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def ipv6_linklocal_addr(self) -> str:
        """
        This generates a link local v6 address from ipv6_ipam_id. This is needed for VRRP.
        """
        # example if v6 addr is 2001:770:50::4/64
        # should return fe80::770:50:4/64
        if self.ipv6_ipam_id:
            v6_addr = str(get_ip_address(id=self.ipv6_ipam_id))
            return (v6_addr.replace("::", ":")).replace("2001:", "fe80::")
        return None
