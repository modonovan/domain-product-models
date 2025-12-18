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

""" L2VPN Port-to-Port service, for use by clients """

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from products.product_blocks.l2vpn_pp_virtual_circuit import (
    L2vpnPPVirtualCircuitBlock,
    L2vpnPPVirtualCircuitBlockInactive,
    L2vpnPPVirtualCircuitBlockProvisioning,
)


class L2vpnPPInactive(SubscriptionModel, is_base=True):
    """
    This is the base model for L2VPN Port-to-Port service subscriptions.
    """

    virtual_circuit: L2vpnPPVirtualCircuitBlockInactive

    @property
    def netbox_service_type(self) -> str:
        return "vpn/l2vpns"


class L2vpnPPProvisioning(L2vpnPPInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the L2VPN Port-to-Port service.
    """

    virtual_circuit: L2vpnPPVirtualCircuitBlockProvisioning


class L2vpnPP(L2vpnPPProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the L2VPN Port-to-Port service.
    """

    virtual_circuit: L2vpnPPVirtualCircuitBlock
