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

""" Core Link virtual circuit, used by Core Link """

from typing import Annotated

from annotated_types import Len
from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SI, SubscriptionLifecycle
from pydantic import computed_field

from products.product_blocks.core_sap import (
    CoreSAPBlock,
    CoreSAPBlockInactive,
    CoreSAPBlockProvisioning,
)

ListOfSaps = Annotated[list[SI], Len(min_length=2, max_length=2)]

class CoreVirtualCircuitBlockInactive(ProductBlockModel, product_block_name="CoreVirtualCircuit"):
    """
    This is the inactive version of the Core Virtual Circuit product block.
    """

    # reference to NetBox cable object
    ims_id: int | None = None
    # reference to NetBox prefix object
    ipv4_prefix_id: int | None = None
    # reference to NetBox prefix object
    ipv6_prefix_id: int | None = None
    # random char string - in our case used for IS-IS authentication and we automatically generate it via orchestrator
    # in the pydantic form. This is optional for the user to fill in.
    auth_key: str | None = None
    isis_metric: int | None = None
    mtu: int | None = None
    speed: int | None = None
    # Port subscriptions
    saps: ListOfSaps[CoreSAPBlockInactive]


class CoreVirtualCircuitBlockProvisioning(
    CoreVirtualCircuitBlockInactive,
    lifecycle=[SubscriptionLifecycle.PROVISIONING],
):
    """
    This is the provisioning version of the Core Virtual Circuit product block.
    It represents a Core Virtual Circuit that is in the process of being provisioned.
    We like to think of it as being "almost there" but not yet fully active. In this state, all required fields should be populated to facilitate successful provisioning.
    """

    ims_id: int | None = None
    ipv4_prefix_id: int | None = None
    ipv6_prefix_id: int | None = None
    auth_key: str | None = None
    isis_metric: int | None = None
    mtu: int | None = None
    speed: int | None = None
    saps: ListOfSaps[CoreSAPBlockProvisioning]

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        #TODO fill me in
        """
        return "Core VC Block"



class CoreVirtualCircuitBlock(
    CoreVirtualCircuitBlockProvisioning,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    """
    This is the active version of the Core Virtual Circuit product block.
    It represents a Core Virtual Circuit that is fully provisioned and active.
    In this state, all required fields must be populated, and the Core Virtual Circuit is operational within the ASIERA service.
    """

    ims_id: int
    ipv4_prefix_id: int | None = None
    ipv6_prefix_id: int | None = None
    auth_key: str | None = None
    isis_metric: int | None = None
    mtu: int
    speed: int | None = None
    saps: ListOfSaps[CoreSAPBlock]
