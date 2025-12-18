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

"""IP Transit virtual circuit, used by all IPT products"""

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field

from products.product_blocks.sap_ipt import (
    SAPIPTBlock,
    SAPIPTBlockInactive,
    SAPIPTBlockProvisioning,
)


class IPTVirtualCircuitBlockInactive(
    ProductBlockModel, product_block_name="IPTVirtualCircuit"
):
    """
    This block represents an IPT Virtual Circuit in its inactive state.
    It contains references to NetBox objects and configuration parameters
    that will be used when the subscription is activated.
    """

    # reference to NetBox circuit object
    ims_id: int | None = None
    # reference to NetBox virtual circuit object
    ims_vc_id: int | None = None
    # reference to NetBox prefix object
    ipv4_prefix_id: int | None = None
    # reference to NetBox prefix object
    ipv6_prefix_id: int | None = None
    # ASN
    peer_as: str | None = None
    # HIGH|LOW|HIGHER|LOWER
    # This defines whether or not the import/export policy will prefer this circuit over others
    # In ASIERA we use the following mapping for local preference for example:
    # HIGHER -> 450
    # HIGH   -> 400
    # LOW    -> 300
    # LOWER  -> 250
    # This is a choice list in the UI
    policy: str | None = None
    # random char string which is used to authenticate BGP peers. We use MD5 authentication and this
    # key is configured on both sides of the BGP session. The key itself is auto-generated
    # and stored securely. The form allows a user to create a new key or leave it empty to
    # keep the existing key.
    auth_key: str | None = None
    # VRRP only config
    vrrp_priority: int | None = None
    vrrp_hold_time: int | None = None
    # Port subscription
    sap: SAPIPTBlockInactive

    @property
    def local_preference(self) -> int:
        match self.policy:
            case "HIGHER":
                return 450
            case "HIGH":
                return 400
            case "LOW":
                return 300
            case "LOWER":
                return 250
            case _:
                raise Exception("Unknown policy")


class IPTVirtualCircuitBlockProvisioning(
    IPTVirtualCircuitBlockInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This block represents an IPT Virtual Circuit in its provisioning state.
    """

    ims_id: int | None = None
    ims_vc_id: int | None = None
    ipv4_prefix_id: int | None = None
    ipv6_prefix_id: int | None = None
    peer_as: str | None = None
    policy: str | None = None
    auth_key: str | None = None
    vrrp_priority: int | None = None
    vrrp_hold_time: int | None = None
    sap: SAPIPTBlockProvisioning

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        Title used in the UI to represent this block
        """
        return "IPT  VC Block"

    @property
    def local_preference(self) -> int:
        match self.policy:
            case "HIGHER":
                return 450
            case "HIGH":
                return 400
            case "LOW":
                return 300
            case "LOWER":
                return 250
            case _:
                raise Exception("Unknown policy")


class IPTVirtualCircuitBlock(
    IPTVirtualCircuitBlockProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This block represents an IPT Virtual Circuit in its active state.
    """

    ims_id: int | None = None
    ims_vc_id: int | None = None
    # will be null for VRRP IPT
    ipv4_prefix_id: int | None = None
    # will be null for VRRP IPT
    ipv6_prefix_id: int | None = None
    peer_as: str
    policy: str
    # will be null for Static IPT
    auth_key: str | None = None
    # will be null for all except VRRP
    vrrp_priority: int | None = None
    vrrp_hold_time: int | None = None
    sap: SAPIPTBlock

    @property
    def local_preference(self) -> int:
        match self.policy:
            case "HIGHER":
                return 450
            case "HIGH":
                return 400
            case "LOW":
                return 300
            case "LOWER":
                return 250
            case _:
                raise Exception("Unknown policy")
