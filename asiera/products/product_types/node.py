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

""" Device subscription, representing a router, switch or firewall. Only used by ASIERA. """

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle, strEnum

from products.product_blocks.node import (
    NodeBlock,
    NodeBlockInactive,
    NodeBlockProvisioning,
)


class NodeType(strEnum):
    """
    Node type for the Node service.
    Currently ASIERA only supports Juniper and Arista devices as these are the device types deployed on the network.
    """

    Juniper = "Juniper"
    Arista = "Arista"


class NodeInactive(SubscriptionModel, is_base=True):
    """
    This is the base class for Node subscriptions in an inactive state.
    """

    node_type: NodeType
    node: NodeBlockInactive


class NodeProvisioning(NodeInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the Node service.
    """

    node_type: NodeType
    node: NodeBlockProvisioning

    @property
    def platform(self) -> str:
        match self.node_type:
            case "Juniper":
                return "Juniper Junos"
            case "Arista":
                return "Arista EOS"
            case _:
                return "Platform not supported for this NodeType"


class Node(NodeProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the Node service.
    """

    node_type: NodeType
    node: NodeBlock
