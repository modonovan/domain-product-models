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

""" L2VPN SAP, representing a L2VPN termination in Netbox. Used by L2VPN PP and PV """

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


class SAPPPBlockInactive(ProductBlockModel, product_block_name="SAPPP"):
    """
    #TODO fill me in
    """

    port: PortBlockInactive | LAGPortBlockInactive | None = None
    ims_id: int | None = None
    mtu: int | None = None


class SAPPPBlockProvisioning(SAPPPBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    port: PortBlockProvisioning | LAGPortBlockProvisioning
    ims_id: int | None = None
    mtu: int

    @computed_field  # type: ignore[misc]
    @property
    def title(self) -> str:
        """
        #TODO fill me in
        """
        return f"Port {self.port.port_name} on {self.port.node.node_name}"


class SAPPPBlock(SAPPPBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    port: PortBlock | LAGPortBlock
    ims_id: int
    mtu: int
