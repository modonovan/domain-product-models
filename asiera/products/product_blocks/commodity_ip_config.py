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

""" Commodity IP config, used by Commodity IP """

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field


class CommodityIPConfigInactive(ProductBlockModel, product_block_name="CommodityIPConfig"):
    """
    This class/function is used to define the inactive state of the Commodity IP Config product block.
    It contains optional fields for cip_rate_limit and cip_burst_limit, which can be set.
    The ASIERA Commodity IP product allows our clients to subrate their internet connections and this is generally used
    on tagged interfaces.
    """

    cip_rate_limit: int | None = None
    cip_burst_limit: int | None = None


class CommodityIPConfigProvisioning(
    CommodityIPConfigInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This is the provisioning version of the Commodity IP Config product block.
    It represents a Commodity IP Config that is in the process of being provisioned.
    We like to think of it as being "almost there" but not yet fully active. In this state, all required fields should be populated to facilitate successful provisioning.
    """

    cip_rate_limit: int | None = None
    cip_burst_limit: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        The title of the product block.
        """
        return "Commodity IP Config Block"


class CommodityIPConfig(
    CommodityIPConfigProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This is the active version of the Commodity IP Config product block.
    It represents a Commodity IP Config that is fully provisioned and active.
    In this state, all required fields must be populated, and the Commodity IP Config is operational within the ASIERA service.
    """

    cip_rate_limit: int
    cip_burst_limit: int
