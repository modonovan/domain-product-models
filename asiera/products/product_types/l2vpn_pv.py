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

""" L2VPN Port-to-VLAN service, for use by clients """

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from products.product_blocks.l2vpn_pv_virtual_circuit import (
    L2vpnPVVirtualCircuitBlock,
    L2vpnPVVirtualCircuitBlockInactive,
    L2vpnPVVirtualCircuitBlockProvisioning,
)


class L2vpnPVInactive(SubscriptionModel, is_base=True):
    """
    #TODO fill me in
    """

    virtual_circuit: L2vpnPVVirtualCircuitBlockInactive

    @property
    def netbox_service_type(self) -> str:
        return "vpn/l2vpns"


class L2vpnPVProvisioning(L2vpnPVInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    virtual_circuit: L2vpnPVVirtualCircuitBlockProvisioning


class L2vpnPV(L2vpnPVProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    virtual_circuit: L2vpnPVVirtualCircuitBlock
