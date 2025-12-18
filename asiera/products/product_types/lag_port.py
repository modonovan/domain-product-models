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

""" Interface subscription, representing a LAG port. This iteration of the LAG product type is for client facing LAGs only. """

from typing import Annotated
from annotated_types import Len
from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SI, SubscriptionLifecycle
from services import netbox

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

ListOfChildPorts = Annotated[list[SI], Len(min_length=0)]

class LAGPortInactive(SubscriptionModel, is_base=True):
    """
    This is the inactive state of the LAG Port service.
    """

    port: LAGPortBlockInactive
    child_ports: ListOfChildPorts[PortBlockInactive]

    @property
    def speed(self) -> str:
        speed = 0
        for child_port in self.child_ports:
            child_port_speed = netbox.get_interface(id=child_port.ims_id).speed
            if child_port_speed != None:
                speed = speed + child_port_speed
        return speed


class LAGPortProvisioning(LAGPortInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the LAG Port service.
    """

    port: LAGPortBlockProvisioning
    child_ports: ListOfChildPorts[PortBlockProvisioning]


class LAGPort(LAGPortProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
   This is the active state of the LAG Port service.
    """

    port: LAGPortBlock
    child_ports: ListOfChildPorts[PortBlock]