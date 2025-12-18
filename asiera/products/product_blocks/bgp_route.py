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

"""
    BGP route, used by IPT eBGP product. In asiera, BGP routes are represented as separate product blocks.
    This module defines the data models for BGP route product blocks across different subscription lifecycles.
    This product ultimately links to IMS Prefix objects representing the BGP routes in the IMS. These prefixes or BGP routes
    are associated with neighbors (next-hops) defined in IPT eBGP Neighbor product blocks. This modular approach allows for flexible
    management of BGP routes within the IPT eBGP service and ultimately gives us the capability to map any BGP route to any service subscription.
"""

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field


class BgpRouteBlockInactive(ProductBlockModel, product_block_name="BgpRoute"):
    """
    This is the inactive version of the BGP Route product block. It serves as a draft or placeholder for BGP route configurations
    that are not yet active. In this state, the product block may lack certain required fields that are necessary for provisioning and activation.
    """

    ims_prefix_id: int | None = None
    # [v4/v6]
    ip_version: int | None = None
    # destination - next-hop
    neighbor_id: int | None = None


class BgpRouteBlockProvisioning(
    BgpRouteBlockInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This is the provisioning version of the BGP Route product block. It represents a BGP route that is in the process of being provisioned.
    We like to think of it as being "almost there" but not yet fully active. In this state, all required fields should be populated to facilitate successful provisioning.
    """

    ims_prefix_id: int | None = None
    ip_version: int | None = None
    neighbor_id: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        Title of the BGP Route product block.
        """
        return "IPT BGP Route"


class BgpRouteBlock(
    BgpRouteBlockProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This is the active version of the BGP Route product block. It represents a BGP route that is fully provisioned and active.
    In this state, all required fields must be populated, and the BGP route is operational within the IPT eBGP service and the prefix(es) exist in the IMS with a status of "active".
    """

    ims_prefix_id: int
    ip_version: int
    neighbor_id: int
