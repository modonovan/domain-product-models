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

"""This module registers all Asiera product types in the orchestrator's
subscription model registry. Workflow Orchestrator uses this registry to map
product type names to their corresponding classes. Without this registration,
the orchestrator would not be able to recognise or manage these product types and
thus would not be able to handle subscriptions related to them. No registration
means no building a workflow for them.
"""

from orchestrator.domain import SUBSCRIPTION_MODEL_REGISTRY

from products.product_types.core_link import CoreLink
from products.product_types.core_port import CorePort
from products.product_types.ip_prefix import IpPrefix
from products.product_types.ipt_static import IPTStatic
from products.product_types.ipt_ebgp import IPTeBGP
from products.product_types.ipt_vrrp import IPTVRRP
from products.product_types.commodity_ip import CommodityIP
from products.product_types.l2vpn_pp import L2vpnPP
from products.product_types.l2vpn_vv import L2vpnVV
from products.product_types.l2vpn_pv import L2vpnPV
from products.product_types.l2vpn_vv_translation import L2vpnVVTranslation
from products.product_types.l3vpn import L3vpn
from products.product_types.node import Node
from products.product_types.port import Port
from products.product_types.lag_port import LAGPort
from products.product_types.core_lag_port import CoreLAGPort


SUBSCRIPTION_MODEL_REGISTRY.update(
    {
        "node Juniper": Node,
        "node Arista": Node,
        "port 1G": Port,
        "port 10G": Port,
        "port 40G": Port,
        "port 100G": Port,
        "port 400G": Port,
        "LAG Port": LAGPort,
        "core port 1G": CorePort,
        "core port 10G": CorePort,
        "core port 40G": CorePort,
        "core port 100G": CorePort,
        "core port 400G": CorePort,
        "core link": CoreLink,
        "core LAG port": CoreLAGPort,
        "IPT static": IPTStatic,
        "IPT eBGP": IPTeBGP,
        "IPT VRRP": IPTVRRP,
        "Commodity IP": CommodityIP,
        "L2VPN Port-to-Port": L2vpnPP,
        "L2VPN VLAN-to-VLAN": L2vpnVV,
        "L2VPN Port-to-VLAN": L2vpnPV,
        "L2VPN with VLAN translation": L2vpnVVTranslation,
        "L3 VPN": L3vpn,
        "IPv4 Prefix (LIR Allocation)": IpPrefix,
        "IPv6 Prefix (LIR Allocation)": IpPrefix,
    }
)
