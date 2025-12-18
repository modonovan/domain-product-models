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


from orchestrator.domain import SubscriptionModel

from products.product_blocks.l2vpn_pp_virtual_circuit import (
    L2vpnPPVirtualCircuitBlockProvisioning,
)
from products.services.description import description
from services import netbox


def build_l2vpn_payload(
    model: L2vpnPPVirtualCircuitBlockProvisioning,
    subscription: SubscriptionModel,
) -> netbox.L2vpnPayload:
    """Create and return a Netbox payload object for a
       :class:`~products.product_blocks.virtual_circuit.L2vpnPPVirtualCircuitBlockProvisioning`.

    Example payload::

       {
          "vid": 4,
          "name": "paris01a 0/0/1 vlan 4",
          "status": "active"
       }

    Args:
        model: VirtualCircuitBlockProvisioning
        subscription: The Subscription that will be provisioned

    Returns: :class:`netbox.L2vpnPayload`

    """
    return netbox.L2vpnPayload(
        name=f"{description(subscription)}",
        slug=str(subscription.subscription_id),
        tenant=subscription.customer_id,
        identifier=subscription.virtual_circuit.vc_id,
    )
