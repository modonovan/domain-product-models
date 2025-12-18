
"""
L3VPN service, for use by clients
Currently only used for Educampus and Gov't Networks
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
    #TODO fill me in
    """

    l3vpn_config: L3VPNConfigInactive
    saps: ListOfSaps[SAPL3VPNBlockInactive]

    @property
    def netbox_service_type(self) -> str:
        return "ipam/vrfs"


class L3vpnProvisioning(L3vpnInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """
    #TODO fill me in
    """

    l3vpn_config: L3VPNConfigProvisioning
    saps: ListOfSaps[SAPL3VPNBlockProvisioning]


class L3vpn(L3vpnProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """
    #TODO fill me in
    """

    l3vpn_config: L3VPNConfig
    saps: ListOfSaps[SAPL3VPNBlock]
 