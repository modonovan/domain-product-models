# ASIERA (formerly HEAnet) products including product blocks and types

## Our setup

In ASIERA, we have implemented Workflow Orchestrator in conjunction with NetBox as our IMS of choice. NetBox is the SoT (Source of Truth) for much of our data but we do store certain chosen elements within the Orchestrator data base subscriptions tables for strategic reasons.

In the case where we don't store data itself in the Orchestrator database but rather the data is in NetBox (or maybe our CRM system in the case of our Customer List), we instead store pointers in the Orchestrator database towards the actual data in the NetBox database e.g. rather than storing an actual IPv4 of IPv6 address for a device or interface etc we will store the ID of the address in NetBox. This allows us the flexibility to achieve Single Sources of Truth for our data where possible.

## What about the "services" directory?

In our models, we have also included a "services" directory. We have done this to add an element of repeatability to the payloads we send into NetBox for the various subscription types we have. We also customise the generic NetBox interactions by registering specific endpoints we may wish to send payloads to via the NetBox API. This also allows us to better manage our NetBox Plugins and indeed ensure that a NetBox version update that effects a particular plugin or standard endpoint can be updated and catered for in one place.
