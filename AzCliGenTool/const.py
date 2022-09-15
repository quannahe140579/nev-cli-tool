from enum import Enum


class VirtualNetwork:
    CREATE_PREFIX = "az network vnet create"

    class CreateCli(Enum):
        NAME = "--name"
        ADDRESS_PREFIX = "--address-prefixes"
        RESOURCE_GROUP = "--resource-group"
        LOCATION = "--location"
        DDOS_PROTECTION = "--ddos-protection"
        DDOS_PROTECTION_PLAN = "--ddos-protection-plan"
        DNS_SERVER = "--dns-servers"


class ResourceGroup:
    CREATE_PREFIX = "az group create"

    class CreateCli(Enum):
        NAME = "--name"
        LOCATION = "--location"


class Subnet:
    CREATE_PREFIX = "az network vnet subnet create"

    class CreateCli(Enum):
        ADDRESS_PREFIX = "--address-prefixes"
        NAME = "--name"
        RESOURCE_GROUP = "--resource-group"
        VNET = "--vnet-name"
