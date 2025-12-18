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

from products.product_types.l2vpn_vv import L2vpnVVProvisioning
from products.product_types.l2vpn_pp import L2vpnPPProvisioning
from products.product_types.l2vpn_pv import L2vpnPVProvisioning
from products.product_types.core_link import CoreLinkProvisioning
from products.product_types.l2vpn_vv_translation import (
    L2vpnVVTranslationProvisioning,
)
from products.product_types.l3vpn import L3vpnProvisioning
from products.product_types.ipt_static import IPTStaticProvisioning
from products.product_types.ipt_ebgp import IPTeBGPProvisioning
from products.product_types.ipt_vrrp import IPTVRRPProvisioning
from products.product_types.commodity_ip import CommodityIPProvisioning
from utils.singledispatch import single_dispatch_base

# for fetching site names for L2VPN title
from services import netbox


@singledispatch
def title(model: Union[ProductModel, ProductBlockModel, SubscriptionModel]) -> str:
    """Build subscription title (generic function).

    Specific implementations of this generic function will specify the model types they work on.

    Args:
        model: Domain model for which to construct a title.

    Returns:
    ---
        The constructed title.

    Raises:
    --
        TypeError: in case a specific implementation could not be found. The domain model it was called for will be
            part of the error message.

    """
    return single_dispatch_base(title, model)


### IPT
def ipt_title(ipt: SubscriptionModel) -> str:
    sites = ""
    # get port.node.site from netbox
    slug = netbox.get_device(name=ipt.virtual_circuit.sap.port.node.node_name).site.slug
    sites = sites + slug + "."
    # e.g. $SITENAME_FROM_IMS.ipt.$SHORTENED_UUID
    # - where $SITENAME_FROM_IMS is the site slug from NetBox (which is our IMS of choice)
    # - and $SHORTENED_UUID is the first 8 characters of the subscription UUID
    return f"{sites}ipt.{str(ipt.subscription_id)[:8]}"


@title.register
def _(ipt_static: IPTStaticProvisioning) -> str:
    return ipt_title(ipt_static)


@title.register
def _(ipt_ebgp: IPTeBGPProvisioning) -> str:
    return ipt_title(ipt_ebgp)


@title.register
def _(ipt_vrrp: IPTVRRPProvisioning) -> str:
    sites = ""
    # get port.node.site from netbox
    slug = netbox.get_device(name=ipt_vrrp.circuit_a.sap.port.node.node_name).site.slug
    sites = sites + slug + "."
    # e.g. $SITENAME_FROM_IMS.ipt.$SHORTENED_UUID
    # - where $SITENAME_FROM_IMS is the site slug from NetBox
    # - and $SHORTENED_UUID is the first 8 characters of the subscription UUID
    return f"{sites}ipt.{str(ipt_vrrp.subscription_id)[:8]}"


@title.register
def _(cip: CommodityIPProvisioning) -> str:
    sites = ""
    # get port.node.site from netbox
    slug = netbox.get_device(name=cip.circuit_a.sap.port.node.node_name).site.slug
    sites = sites + slug + "."
    # e.g. $SITENAME_FROM_IMS.ipt.$SHORTENED_UUID
    # - where $SITENAME_FROM_IMS is the site slug from NetBox
    # - and $SHORTENED_UUID is the first 8 characters of the subscription UUID
    return f"{sites}ipt.{str(cip.subscription_id)[:8]}"


### L2VPNs
def l2vpn_title(l2vpn: SubscriptionModel) -> str:
    sites = ""
    for sap in l2vpn.virtual_circuit.saps:
        # get site slugs from netbox
        slug = netbox.get_device(name=sap.port.node.node_name).site.slug
        sites = sites + slug + "."
    # e.g. $SITENAME_A_END_FROM_IMS.$SITENAME_Z_END_FROM_IMS.$SHORTENED_UUID
    # - where $SITENAME_A_END_FROM_IMS is the site slug for the A-End site from NetBox
    # - where $SITENAME_Z_END_FROM_IMS is the site slug for the Z-End site from NetBox
    # - and $SHORTENED_UUID is the first 8 characters of the subscription UUID
    return f"{sites}{str(l2vpn.subscription_id)[:8]}"


@title.register
def _(l2vpn: L2vpnPPProvisioning) -> str:
    return l2vpn_title(l2vpn)


@title.register
def _(l2vpn: L2vpnVVProvisioning) -> str:
    return l2vpn_title(l2vpn)


@title.register
def _(l2vpn: L2vpnPVProvisioning) -> str:
    vc = l2vpn.virtual_circuit
    # get site slugs from netbox
    slug_p = netbox.get_device(name=vc.sap_p.port.node.node_name).site.slug
    slug_v = netbox.get_device(name=vc.sap_v.port.node.node_name).site.slug
    # e.g. $SITENAME_A_END_FROM_IMS.$SITENAME_Z_END_FROM_IMS.$SHORTENED_UUID
    # - where $SITENAME_A_END_FROM_IMS is the site slug for the A-End site from NetBox
    # - where $SITENAME_Z_END_FROM_IMS is the site slug for the Z-End site from NetBox
    # - and $SHORTENED_UUID is the first 8 characters of the subscription UUID
    return f"{slug_p}.{slug_v}.{str(l2vpn.subscription_id)[:8]}"


@title.register
def _(l2vpn: L2vpnVVTranslationProvisioning) -> str:
    vc = l2vpn.virtual_circuit
    # get site slugs from netbox
    slug_a = netbox.get_device(name=vc.sap_a.port.node.node_name).site.slug
    slug_b = netbox.get_device(name=vc.sap_b.port.node.node_name).site.slug
    # e.g. $SITENAME_A_END_FROM_IMS.$SITENAME_Z_END_FROM_IMS.$SHORTENED_UUID
    # - where $SITENAME_A_END_FROM_IMS is the site slug for the A-End site from NetBox
    # - where $SITENAME_Z_END_FROM_IMS is the site slug for the Z-End site from NetBox
    # - and $SHORTENED_UUID is the first 8 characters of the subscription UUID
    return f"{slug_a}.{slug_b}.{str(l2vpn.subscription_id)[:8]}"



@title.register
def _(l3vpn: L3vpnProvisioning) -> str:
    return f"{l3vpn.l3vpn_config.l3vpn_name}.l3vpn.{str(l3vpn.subscription_id)[:8]}"



@title.register
def _(core_link: CoreLinkProvisioning) -> str:
    sites = ""
    for sap in core_link.virtual_circuit.saps:
        # get site slugs from netbox
        slug = netbox.get_device(name=sap.port.node.node_name).site.slug
        sites = sites + slug + "."
    # e.g. $SITENAME_A_END_FROM_IMS.$SITENAME_Z_END_FROM_IMS.$SHORTENED_UUID
    # - where $SITENAME_A_END_FROM_IMS is the site slug for the A-End site from NetBox
    # - where $SITENAME_Z_END_FROM_IMS is the site slug for the Z-End site from NetBox
    # - and $SHORTENED_UUID is the first 8 characters of the subscription UUID
    return f"{sites}{str(core_link.subscription_id)[:8]}"