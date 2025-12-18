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

from products.product_types.ipt_static import IPTStaticProvisioning
from products.services.description import description
from services import netbox


def build_ipt_static_payload(
    model: IPTStaticProvisioning, subscription: SubscriptionModel
) -> netbox.IPTStaticPayload:
    """Create and return a Netbox payload object for a
       :class:`~products.product_blocks.IPTStaticProvisioning`.

    Example payload::

       {
          "provider": 2,
          "circuit_id": "heanet.ipt.1A3B5C78",
          "status": "active"
       }

    Args:
        model: IPTStaticProvisioning
        subscription: The Subscription that will be provisioned

    Returns: :class:`netbox.IPTStaticPayload`

    """
    return netbox.IPTStaticPayload(
        provider=str(netbox.get_tenant(name="HEAnet").id),
        circuit_id=f"{description(subscription)}",
        type=netbox.get_circuit_type(name="IP Transit").id,
        tenant=subscription.customer_id,
        status="active",
    )
