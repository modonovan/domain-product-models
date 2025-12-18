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

""" Interface subscription, representing a physical port. Only used by HEAnet """

from typing import Annotated
from annotated_types import Len
from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SI, SubscriptionLifecycle
from services import netbox

from products.product_blocks.core_port import (
    CorePortBlock,
    CorePortBlockInactive,
    CorePortBlockProvisioning,
)
from products.product_blocks.core_lag_port import (
    CoreLAGPortBlock,
    CoreLAGPortBlockInactive,
    CoreLAGPortBlockProvisioning,
)

ListOfChildPorts = Annotated[list[SI], Len(min_length=0)]


class CoreLAGPortInactive(SubscriptionModel, is_base=True):
    """
    #TODO fill me in
    """

    port: CoreLAGPortBlockInactive
    child_ports: ListOfChildPorts[CorePortBlockInactive]

    @property
    def speed(self) -> str:
        speed = 0
        for child_port in self.child_ports:
            child_port_speed = netbox.get_interface(id=child_port.ims_id).speed
            if child_port_speed != None:
                speed = speed + child_port_speed
        return speed


class CoreLAGPortProvisioning(CoreLAGPortInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    port: CoreLAGPortBlockProvisioning
    child_ports: ListOfChildPorts[CorePortBlockProvisioning]


class CoreLAGPort(CoreLAGPortProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    port: CoreLAGPortBlock
    child_ports: ListOfChildPorts[CorePortBlock]
