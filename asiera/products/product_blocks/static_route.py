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

""" Static route, used by IPT Static product """

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field


class StaticRouteBlockInactive(ProductBlockModel, product_block_name="StaticRoute"):
    """
    This is a Static Route Block representing a static route in NetBox in an inactive state.
    """

    # Draft product block for STATIC_ROUTE
    # prefix and subnet
    ims_prefix_id: int | None = None
    # [v4/v6]
    ip_version: int | None = None
    # destination - next-hop
    next_hop_id: int | None = None


class StaticRouteBlockProvisioning(
    StaticRouteBlockInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This is a Static Route Block representing a static route in NetBox in a provisioning state.
    """

    ims_prefix_id: int | None = None
    ip_version: int | None = None
    next_hop_id: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        Title used in the UI to represent this block
        """
        return "IPT Static Route"


class StaticRouteBlock(
    StaticRouteBlockProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This is a Static Route Block representing a static route in NetBox in an active state.
    """

    ims_prefix_id: int
    ip_version: int
    next_hop_id: int
