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

""" L2VPN VLAN-to-VLAN service, for use by clients """

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from products.product_blocks.l2vpn_vv_virtual_circuit import (
    L2vpnVVVirtualCircuitBlock,
    L2vpnVVVirtualCircuitBlockInactive,
    L2vpnVVVirtualCircuitBlockProvisioning,
)


class L2vpnVVInactive(SubscriptionModel, is_base=True):
    """
    This is the L2VPN VLAN-to-VLAN service type, for use by clients.
    """

    virtual_circuit: L2vpnVVVirtualCircuitBlockInactive

    @property
    def netbox_service_type(self) -> str:
        return "vpn/l2vpns"


class L2vpnVVProvisioning(L2vpnVVInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the L2VPN VLAN-to-VLAN service.
    """

    virtual_circuit: L2vpnVVVirtualCircuitBlockProvisioning


class L2vpnVV(L2vpnVVProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the L2VPN VLAN-to-VLAN service.
    """

    virtual_circuit: L2vpnVVVirtualCircuitBlock
