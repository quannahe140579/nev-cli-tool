from enum import Enum


class VirtualNetwork:
    CREATE_PREFIX = "az network vnet create "

    class CreateCli(Enum):
        NAME = "--name"
        ADDRESS_PREFIX = "--address-prefixes"
        RESOURCE_GROUP = "--resource-group"
        LOCATION = "--location"
        DDOS_PROTECTION = "--ddos-protection"
        DDOS_PROTECTION_PLAN = "--ddos-protection-plan"
        DNS_SERVER = "--dns-servers"

    class TestCli(Enum):
        RESOURCE_GROUP = "rg_name"
        NAME = "vnet_name"
        LOCATION = "vnet_location"
        ADDRESS_SPACE = "vnet_addressspace"
        DDOS_PROTECTION = "vnet_ddos"
        DNS_SERVER = "vnet_dns"

        TEST_PREFIX = "(Get-AzVirtualNetwork -ResourceGroupName '" + RESOURCE_GROUP + "' -Name '" + NAME + "')"
        DNS_SERVER_TEST_TEMPLATE = TEST_PREFIX + ".DhcpOptions.DnsServers -contains '" + DNS_SERVER + "'"
        TEST_TEMPLATE = TEST_PREFIX + " -ne $null "  + "\n" \
                        + TEST_PREFIX + ".Location -eq '" + LOCATION +"' " + "\n"\
                        + TEST_PREFIX + ".AddressSpace.AddressPrefixes[0] -eq '" + ADDRESS_SPACE + "'" + "\n"\
                        + TEST_PREFIX + ".EnableDdosProtection -eq $false"



class ResourceGroup:
    CREATE_PREFIX = "az group create "

    class CreateCli(Enum):
        NAME = "--name"
        LOCATION = "--location"


class Subnet:
    CREATE_PREFIX = "az network vnet subnet create "

    class CreateCli(Enum):
        ADDRESS_PREFIX = "--address-prefixes"
        NAME = "--name"
        RESOURCE_GROUP = "--resource-group"
        VNET = "--vnet-name"

    class DefaultValue(Enum):
        BASTION_SUBNET_NAME = "AzureBastionSubnet"


class DDosProtectionPlan:
    CREATE_PREFIX = "az network ddos-protection create "

    class CreateCli(Enum):
        NAME = "--name"
        RESOURCE_GROUP = "--resource-group"


class PublicIpAddress:
    CREATE_PREFIX = "az network public-ip create "

    class CreateCli(Enum):
        NAME = "--name"
        RESOURCE_GROUP = "--resource-group"
        VERSION = "--version"
        SKU = "--sku"
        METHOD = "--allocation-method"

    class DefaultValue(Enum):
        VERSION = "IPv4"
        SKU = "Standard"
        METHOD = "Static"


class BastionHost:
    CREATE_PREFIX = "az network bastion create "

    class CreateCli(Enum):
        NAME = "--name"
        PUBLIC_IP = "--public-ip-address"
        RESOURCE_GROUP = "--resource-group"
        VNET = "--vnet-name"
        LOCATION = "--location"


class AzureFireWall:
    CREATE_PREFIX = "az network firewall create "

    class CreateCli(Enum):
        NAME = "--name"
        PUBLIC_IP = "--public-ip-address"
        RESOURCE_GROUP = "--resource-group"
        VNET = "--vnet-name"
        LOCATION = "--location"
        CONF = "--conf-name"

    class DefaultValue(Enum):
        CONF_NAME = "config"
        FIREWALL_SUBNET_NAME = "AzureFirewallSubnet"
