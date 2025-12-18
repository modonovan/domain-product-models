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

"""IP Transit VRRP config, used by IPT VRRP"""

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field
from services.netbox import get_ip_address


class IPTVRRPConfigInactive(ProductBlockModel, product_block_name="IPTVRRPConfig"):
    """
    This block represents an IPT VRRP Config in its inactive state.
    It contains references to NetBox objects and configuration parameters
    that will be used when the subscription is activated.
    """

    vrrp_vip_ipv4_addr_id: int | None = None
    vrrp_vip_ipv6_addr_id: int | None = None
    vrrp_group: int | None = None


class IPTVRRPConfigProvisioning(
    IPTVRRPConfigInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This block represents an IPT VRRP Config in its provisioning state.
    """

    vrrp_vip_ipv4_addr_id: int | None = None
    vrrp_vip_ipv6_addr_id: int | None = None
    vrrp_group: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        Title used in the UI to represent this block
        """
        return "IPT VRRP Config Block"

    @computed_field  # type: ignore[misc]
    @property
    def vrrp_vip_ipv6_linklocal_addr(self) -> str:
        """
        generate link local v6 address from vrrp_vip_ipv6_addr
        """
        if self.vrrp_vip_ipv6_addr_id:
            # example if v6 addr is 2001:770:50::1
            # should return fe80::770:50:1
            if self.vrrp_vip_ipv6_addr_id is None:
                return "v6 VIP not set yet"

            v6_addr = str(
                get_ip_address(id=self.vrrp_vip_ipv6_addr_id).address.split("/")[0]
            )
            return (v6_addr.replace("::", ":")).replace("2001:", "fe80::")
        else:
            return None


class IPTVRRPConfig(
    IPTVRRPConfigProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This block represents an IPT VRRP Config in its active state.
    """

    vrrp_vip_ipv4_addr_id: int
    vrrp_vip_ipv6_addr_id: int | None = None
    vrrp_group: int

    @computed_field  # type: ignore[misc]
    @property
    def vrrp_vip_ipv6_linklocal_addr(self) -> str:
        """
        generate link local v6 address from vrrp_vip_ipv6_addr
        """
        if self.vrrp_vip_ipv6_addr_id and get_ip_address(id=self.vrrp_vip_ipv6_addr_id):
            # example if v6 addr is 2001:770:50::1
            # should return fe80::770:50:1
            v6_addr = str(
                get_ip_address(id=self.vrrp_vip_ipv6_addr_id).address.split("/")[0]
            )
            return (v6_addr.replace("::", ":")).replace("2001:", "fe80::")
        else:
            return None
