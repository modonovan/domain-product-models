
"""
L3VPN service, for use by clients
Currently only used in ASIERA for two specific use cases but it can be expanded to other use cases in the future and is ready for that.
"""
from typing import Annotated
from annotated_types import Len

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SI, SubscriptionLifecycle

from products.product_blocks.l3vpn_config import (
    L3VPNConfig,
    L3VPNConfigInactive,
    L3VPNConfigProvisioning,
)

from products.product_blocks.sap_l3vpn import (
    SAPL3VPNBlock,
    SAPL3VPNBlockInactive,
    SAPL3VPNBlockProvisioning,
)

ListOfSaps = Annotated[list[SI], Len(min_length=0)]

class L3vpnInactive(SubscriptionModel, is_base=True):
    """

    """

    l3vpn_config: L3VPNConfigInactive
    saps: ListOfSaps[SAPL3VPNBlockInactive]

    @property
    def netbox_service_type(self) -> str:
        return "ipam/vrfs"


class L3vpnProvisioning(L3vpnInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    This is the provisioning state of the L3VPN service.
    """

    l3vpn_config: L3VPNConfigProvisioning
    saps: ListOfSaps[SAPL3VPNBlockProvisioning]


class L3vpn(L3vpnProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    This is the active state of the L3VPN service.
    """

    l3vpn_config: L3VPNConfig
    saps: ListOfSaps[SAPL3VPNBlock]
