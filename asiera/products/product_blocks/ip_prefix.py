from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import computed_field

"""
    The IP Prefix product block. ASIERA uses IP Prefixes to manage IP address allocations and assignments within the network infrastructure.
    This product block allows for the configuration and management of IP prefixes (either IPv4 or IPv6),
    including details such as prefix length, assignment status, and associated metadata.
    It is essential for ensuring efficient IP address utilization and supporting network services that rely on specific IP addressing schemes.
    It also always us to operate the network in line with RIR policies via our LIR.
    NetBox IPAM integration is used to manage the actual prefixes and IP addresses.
    Once an IP Prefix subscription is active, it can become (for example) a BGP Route subscription or be assigned to a SAP product block.
"""

class IpPrefixBlockInactive(ProductBlockModel, product_block_name="Ip Prefix"):
    aggregate_block: int | None = None
    to_internet: bool | None = True
    autoassign_prefix: bool | None = True
    manually_assigned_prefix: str | None = None
    assigned_ip_prefix: str | None = None
    lir_prefix_ipam_id: int | None = None
    prefix_length: int | None = None
    # This extra information field can be used to simply add a description to the prefix/prefix allocation in our IPAM.
    # In case where an INETNUM or INET6NUM object should exist in the RIR database, this field can be used to store the necessary information.
    extra_information: str | None = None
    # Contact details for RIR database objects - specifically tech-c and admin-c
    tech_c: str | None = None
    admin_c: str | None = None


class IpPrefixBlockProvisioning(IpPrefixBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    aggregate_block: int | None = None
    to_internet: bool | None = True
    autoassign_prefix: bool | None = True
    manually_assigned_prefix: str | None = None
    assigned_ip_prefix: str | None = None
    lir_prefix_ipam_id: int | None = None
    prefix_length: int | None = None
    # This extra information field can be used to simply add a description to the prefix/prefix allocation in our IPAM.
    # In case where an INETNUM or INET6NUM object should exist in the RIR database, this field can be used to store the necessary information.
    extra_information: str
    # Contact details for RIR database objects - specifically tech-c and admin-c
    tech_c: str
    admin_c: str

    @computed_field
    @property
    def title(self) -> str:
        """
        The title of the IP Prefix product block.
        """
        return f"{self.name}"


class IpPrefixBlock(IpPrefixBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    aggregate_block: int
    to_internet: bool
    autoassign_prefix: bool
    manually_assigned_prefix: str | None = None
    assigned_ip_prefix: str
    lir_prefix_ipam_id: int
    prefix_length: int
    # This extra information field can be used to simply add a description to the prefix/prefix allocation in our IPAM.
    # In case where an INETNUM or INET6NUM object should exist in the RIR database, this field can be used to store the necessary information.
    extra_information: str
    # Contact details for RIR database objects - specifically tech-c and admin-c
    tech_c: str
    admin_c: str
