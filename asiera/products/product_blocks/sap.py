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

""" Generic Service Attach Point. Not used at present in the ASIERA products. """

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


class SAPBlockInactive(ProductBlockModel, product_block_name="SAP"):
    """
    #TODO fill me in
    """

    port: PortBlockInactive | LAGPortBlockInactive | None = None
    vlan: int | None = None
    ims_id: int | None = None


class SAPBlockProvisioning(SAPBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    port: PortBlockProvisioning | LAGPortBlockProvisioning
    vlan: int
    ims_id: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        #TODO fill me in
        """
        return f"VLAN {self.vlan} on port {self.port.port_name} on {self.port.node.node_name}"


class SAPBlock(SAPBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    port: PortBlock | LAGPortBlock
    vlan: int
    ims_id: int
