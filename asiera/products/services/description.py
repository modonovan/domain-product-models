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


from functools import singledispatch
from typing import Union

from orchestrator.domain.base import (
    ProductBlockModel,
    ProductModel,
    SubscriptionModel,
)

from products.product_types.core_port import CorePortProvisioning
from products.product_types.core_lag_port import CoreLAGPortInactive
from products.product_types.core_link import CoreLinkProvisioning
from products.product_types.ip_prefix import IpPrefixProvisioning
from products.product_types.ipt_static import IPTStaticProvisioning
from products.product_types.ipt_ebgp import IPTeBGPProvisioning
from products.product_types.ipt_vrrp import IPTVRRPProvisioning
from products.product_types.commodity_ip import CommodityIPProvisioning
from products.product_types.l2vpn_vv import L2vpnVVProvisioning
from products.product_types.l2vpn_pp import L2vpnPPProvisioning
from products.product_types.l2vpn_pv import L2vpnPVProvisioning
from products.product_types.l2vpn_vv_translation import (
    L2vpnVVTranslationProvisioning,
)
from products.product_types.l3vpn import L3vpnProvisioning
from products.product_types.node import NodeProvisioning
from products.product_types.port import PortProvisioning
from products.product_types.lag_port import LAGPortInactive
from products.services.title import title
from services import netbox
from utils.singledispatch import single_dispatch_base

# for debug logging
# import structlog
# logger = structlog.get_logger(__name__)


@singledispatch
def description(model: Union[ProductModel, ProductBlockModel, SubscriptionModel]) -> str:
    """Build subscription description (generic function).

    Specific implementations of this generic function will specify the model types they work on.

    Args:
        model: Domain model for which to construct a description.

    Returns:
    ---
        The constructed description.

    Raises:
    --
        TypeError: in case a specific implementation could not be found. The domain model it was called for will be
            part of the error message.

    """
    return single_dispatch_base(description, model)


@description.register
def _(ip_prefix: IpPrefixProvisioning) -> str:
    return f"Prefix allocation for  {ip_prefix.ip_prefix.assigned_ip_prefix}"


@description.register
def _(node: NodeProvisioning) -> str:
    return f"node {node.node.node_name} ({node.node.node_status})"


@description.register
def _(port: PortProvisioning) -> str:
    return f"{port.product.name} {port.port.node.node_name} {port.port.port_name}"


@description.register
def _(lag_port: LAGPortInactive) -> str:
    return f"{lag_port.product.name} {lag_port.port.node.node_name} {lag_port.port.port_name}"


@description.register
def _(core_link: CoreLinkProvisioning) -> str:
    return (
        f"{title(core_link)} "
        f"{core_link.virtual_circuit.saps[0].port.node.node_name} {core_link.virtual_circuit.saps[0].port.port_name}"
        " <-> "
        f"{core_link.virtual_circuit.saps[1].port.port_name} {core_link.virtual_circuit.saps[1].port.node.node_name}"
    )


@description.register
def _(core_port: CorePortProvisioning) -> str:
    return f"{core_port.product.name} {core_port.port.node.node_name} {core_port.port.port_name}"


@description.register
def _(core_lag_port: CoreLAGPortInactive) -> str:
    return f"{core_lag_port.product.name} {core_lag_port.port.node.node_name} {core_lag_port.port.port_name}"

@description.register
def _(ipt_static: IPTStaticProvisioning) -> str:
    # get speed of parent interface from netbox
    # divide by 1000 to get Mbit/s figure
    speed = str(
        int(int(netbox.get_interface(id=ipt_static.virtual_circuit.sap.port.ims_id).speed) / 1000)
    )
    # e.g. SOMESITE.ipt.387aff5a :: IPTStatic 1000 Mbit/s
    return f"{title(ipt_static)} :: " f"{ipt_static.product.tag} " f"{speed} Mbit/s"


@description.register
def _(cip: CommodityIPProvisioning) -> str:
    # get speed of parent interface from netbox
    # divide by 1000 to get Mbit/s figure
    speed = str(
        int(int(netbox.get_interface(id=cip.circuit_a.sap.port.ims_id).speed) / 1000)
    )
    # e.g. SOMESITE.ipt.387aff5a :: IPTStatic 1000 Mbit/s
    return f"{title(cip)} :: " f"{cip.product.tag} " f"{speed} Mbit/s"


@description.register
def _(ipt_vrrp: IPTVRRPProvisioning) -> str:
    # get speed of parent interface from netbox
    # divide by 1000 to get Mbit/s figure
    speed = str(
        int(int(netbox.get_interface(id=ipt_vrrp.circuit_a.sap.port.ims_id).speed) / 1000)
    )
    # e.g. SOMESITE.ipt.387aff5a :: IPTStatic 1000 Mbit/s
    return f"{title(ipt_vrrp)} :: " f"{ipt_vrrp.product.tag} " f"{speed} Mbit/s"


@description.register
def _(ipt_ebgp: IPTeBGPProvisioning) -> str:
    # get speed of parent interface from netbox
    # divide by 1000 to get Mbit/s figure
    speed = str(
        int(int(netbox.get_interface(id=ipt_ebgp.virtual_circuit.sap.port.ims_id).speed) / 1000)
    )
    # e.g. SOMESITE.ipt.387aff5a :: IPTStatic 1000 Mbit/s
    return f"{title(ipt_ebgp)} :: " f"{ipt_ebgp.product.tag} " f"{speed} Mbit/s"


@description.register
def _(l3vpn: L3vpnProvisioning) -> str:
    return f"{title(l3vpn)} :: " f"{l3vpn.product.tag} "


def l2vpn_description(l2vpn: SubscriptionModel) -> str:
    # e.g. SOMESITE_A.SOMESITE_Z.387aff5a :: L2VPNPP 1000 Mbit/s
    return f"{title(l2vpn)} :: " f"{l2vpn.product.tag} " f"{l2vpn.virtual_circuit.speed} Mbit/s"


@description.register
def _(l2vpn: L2vpnPPProvisioning) -> str:
    # e.g. SOMESITE_A.SOMESITE_Z.387aff5a :: L2VPNPP 1000 Mbit/s
    return l2vpn_description(l2vpn)


@description.register
def _(l2vpn: L2vpnVVProvisioning) -> str:
    # e.g. SOMESITE_A.SOMESITE_Z.387aff5a :: L2VPNVV 1000 Mbit/s
    return l2vpn_description(l2vpn)


@description.register
def _(l2vpn: L2vpnPVProvisioning) -> str:
    # e.g. SOMESITE_A.SOMESITE_Z.387aff5a :: L2VPNPV 1000 Mbit/s
    return l2vpn_description(l2vpn)


@description.register
def _(l2vpn: L2vpnVVTranslationProvisioning) -> str:
    # e.g. SOMESITE_A.SOMESITE_Z.387aff5a :: L2VPNPV 1000 Mbit/s
    return l2vpn_description(l2vpn)
