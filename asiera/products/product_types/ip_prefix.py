from enum import StrEnum

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from products.product_blocks.ip_prefix import IpPrefixBlock, IpPrefixBlockInactive, IpPrefixBlockProvisioning


class AddressFamily(StrEnum):
    IPv4 = "IPv4"
    IPv6 = "IPv6"


class IpPrefixInactive(SubscriptionModel, is_base=True):
    address_family: AddressFamily
    ip_prefix: IpPrefixBlockInactive


class IpPrefixProvisioning(IpPrefixInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    address_family: AddressFamily
    ip_prefix: IpPrefixBlockProvisioning


class IpPrefix(IpPrefixProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    address_family: AddressFamily
    ip_prefix: IpPrefixBlock
