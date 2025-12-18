###
# this file over-rides WFO's display of "default customer"
# by fetching the customer from Netbox

import strawberry

# for checking ID validity
import re

from orchestrator.graphql.schemas.customer import CustomerType
from orchestrator.graphql.schemas.subscription import (
    SubscriptionInterface,
)
from orchestrator.graphql.utils.override_class import override_class
from services import netbox


async def resolve_customer(root: CustomerType) -> CustomerType:
    # stmt = select(CustomerTable).where(CustomerTable.customer_id == root.customer_id)

    # if not (customer := db.session.execute(stmt).scalars().first()):
    #     return CustomerType(
    #         customer_id=root.customer_id, fullname="missing", shortcode="missing"
    #     )
    customer = None
    if bool(re.search("[a-zA-Z]", root.customer_id)):
        return CustomerType(
            customer_id=0,
            fullname=f"Not valid ID: {root.customer_id}",
            shortcode="missing",
        )
    try:
        customer = netbox.get_tenant(id=root.customer_id)
    except Exception as exc:
        return CustomerType(customer_id=0, fullname=exc, shortcode="missing")
    if customer == None:
        return CustomerType(customer_id=0, fullname="NetBox unreachable", shortcode="missing")
    # should get to here if all went well
    return CustomerType(
        customer_id=root.customer_id,
        fullname=customer.name,
        shortcode=customer.slug.upper(),
    )


# # Create a strawberry field with the resolver for the customer field
customer_field = strawberry.field(
    resolver=resolve_customer, description="Returns customer of a subscription"
)  # type: ignore
# # Assign a new name to the strawberry field; this name will add the 'customer' field in the class
customer_field.name = "customer"

# # Override the SubscriptionInterface and ProcessType with the new 'customer' field
# override_class(ProcessType, [customer_field])
custom_subscription_interface = override_class(SubscriptionInterface, [customer_field])
