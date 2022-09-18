from abc import ABC
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import const
import abc


# Code create Vnet Cli
class Subscription(models.Model):
    name = models.CharField(max_length=100, blank=False, default="MySubscription")
    subscription_id = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name


class AzureBaseModel(models.Model):
    create_cli_text = ""
    test_cli_text = ""

    @abc.abstractmethod
    def generate_create_cli(self):
        pass

    @abc.abstractmethod
    def generate_test_cli(self):
        pass


class CreateCli(models.Model):
    create_cli = models.CharField(max_length=1000, default="123")
    resource_model = models.OneToOneField(AzureBaseModel, on_delete=models.CASCADE)


class TestCli(models.Model):
    test_cli = models.CharField(max_length=1000, default="123")
    resource = models.OneToOneField(AzureBaseModel, on_delete=models.CASCADE)


class ResourceGroup(AzureBaseModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=False)
    # all resource group deleted then location have deleted availability
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=100, blank=False, default="MyResourceGroup", unique=True)

    def generate_create_cli(self):
        cli_text = const.ResourceGroup.CREATE_PREFIX
        if self.location:
            cli_text = cli_text + " " + const.ResourceGroup.CreateCli.LOCATION.value + " " + self.location.name
        if self.name:
            cli_text = cli_text + " " + const.ResourceGroup.CreateCli.NAME.value + " " + self.name
        return cli_text

    def generate_test_cli(self):
        pass

    def __str__(self):
        return self.name

    def save(self):
        self.create_cli_text = self.generate_create_cli()
        self.test_cli_text = "Demo test cli"
        super(ResourceGroup, self).save()


class ResourceBase(AzureBaseModel):
    resource_group = models.ForeignKey(ResourceGroup, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=100, blank=False)

    def generate_create_cli(self):
        pass

    def generate_test_cli(self):
        pass


class PublicIpAddress(ResourceBase):

    def generate_create_cli(self):
        cli_text = const.PublicIpAddress.CREATE_PREFIX
        if self.name:
            cli_text = cli_text + const.PublicIpAddress.CreateCli.NAME.value + " " + self.name + " "
        if self.resource_group:
            cli_text = cli_text + const.PublicIpAddress.CreateCli.RESOURCE_GROUP.value + " " + self.resource_group.name + " "
        cli_text = cli_text + const.PublicIpAddress.CreateCli.VERSION.value + " " + const.PublicIpAddress.DefaultValue.VERSION.value + " "
        cli_text = cli_text + const.PublicIpAddress.CreateCli.SKU.value + " " + const.PublicIpAddress.DefaultValue.SKU.value + " "
        cli_text = cli_text + const.PublicIpAddress.CreateCli.METHOD.value + " " + const.PublicIpAddress.DefaultValue.METHOD.value
        return cli_text

    def save(self):
        self.create_cli_text = self.generate_create_cli()
        super(PublicIpAddress, self).save()


class DdosProtectionPlan(ResourceBase):
    def __str__(self):
        return self.name

    def generate_create_cli(self):
        cli_text = const.DDosProtectionPlan.CREATE_PREFIX
        if self.resource_group:
            cli_text = cli_text + " " + const.DDosProtectionPlan.CreateCli.RESOURCE_GROUP.value + " " + self.resource_group.name
        if self.name:
            cli_text = cli_text + " " + const.DDosProtectionPlan.CreateCli.NAME.value + " " + self.name

        return cli_text

    def save(self):
        self.create_cli_text = self.generate_create_cli()
        super(DdosProtectionPlan, self).save()


def update_test_cli(test_cli_template, district):
    origin = test_cli_template
    for key in district:
        origin = origin.strip().replace(key, district[key])
    return origin


class VirtualNetwork(ResourceBase):
    address_space = models.CharField(max_length=100, blank=False, default="10.0.0.0/16")
    dns_server = models.CharField(max_length=100, blank=True)
    ddos_plan = models.OneToOneField(DdosProtectionPlan, on_delete=models.RESTRICT, null=True, blank=True)

    def generate_create_cli(self):
        cli_text = const.VirtualNetwork.CREATE_PREFIX
        # Code more here
        if self.name:
            cli_text = cli_text + " " + const.VirtualNetwork.CreateCli.NAME.value + " " + self.name + " "
        if self.resource_group:
            cli_text = cli_text + const.VirtualNetwork.CreateCli.RESOURCE_GROUP.value + " " + self.resource_group.name + " "
        if self.address_space:
            cli_text = cli_text + const.VirtualNetwork.CreateCli.ADDRESS_PREFIX.value + " " + self.address_space + " "
        if self.location:
            cli_text = cli_text + const.VirtualNetwork.CreateCli.LOCATION.value + " " + self.location.name + " "
        if self.dns_server:
            cli_text = cli_text + const.VirtualNetwork.CreateCli.DNS_SERVER.value + " " + self.dns_server + " "
        if self.ddos_plan:
            cli_text = cli_text + const.VirtualNetwork.CreateCli.DDOS_PROTECTION.value + " " + "True " \
                       + const.VirtualNetwork.CreateCli.DDOS_PROTECTION_PLAN.value + " " + self.ddos_plan.name
        else:
            cli_text = cli_text + const.VirtualNetwork.CreateCli.DDOS_PROTECTION.value + " " + "False "
        return cli_text

    def generate_test_cli(self):
        test_text = const.VirtualNetwork.TestCli.TEST_TEMPLATE.value
        test_text += const.VirtualNetwork.TestCli.DNS_SERVER_TEST_TEMPLATE.value
        district = {
            const.VirtualNetwork.TestCli.RESOURCE_GROUP.value: self.resource_group.name,
            const.VirtualNetwork.TestCli.NAME.value: self.name,
            const.VirtualNetwork.TestCli.LOCATION.value: self.location.name,
            const.VirtualNetwork.TestCli.ADDRESS_SPACE.value: self.address_space,
            const.VirtualNetwork.TestCli.DNS_SERVER.value: self.dns_server,
        }
        test_text = update_test_cli(test_text, district)
        return test_text

    def save(self):
        self.create_cli_text = self.generate_create_cli()
        self.test_cli_text = self.generate_test_cli()
        super(VirtualNetwork, self).save()

    def __str__(self):
        return self.name


class Subnet(ResourceBase):
    vnet = models.ForeignKey(VirtualNetwork, on_delete=models.CASCADE, null=False, related_name="subnet_list")
    subnet_address = models.CharField(max_length=100, blank=False, default="10.0.0.0/24", unique=True,
                                      verbose_name="Subnet Address Space")

    def generate_create_cli(self):
        cli_text = const.Subnet.CREATE_PREFIX
        if self.name:
            cli_text = cli_text + const.Subnet.CreateCli.NAME.value + " " + self.name + " "
        if self.subnet_address:
            cli_text = cli_text + const.Subnet.CreateCli.ADDRESS_PREFIX.value + " " + self.subnet_address + " "
        if self.resource_group:
            cli_text = cli_text + const.Subnet.CreateCli.RESOURCE_GROUP.value + " " + self.resource_group.name + " "
        if self.vnet:
            cli_text = cli_text + const.Subnet.CreateCli.VNET.value + " " + self.vnet.name + " "
        return cli_text

    def save(self):
        self.create_cli_text = self.generate_create_cli()
        super(Subnet, self).save()


class BastionHost(ResourceBase):
    vnet = models.OneToOneField(VirtualNetwork, on_delete=models.CASCADE, null=False)

    def generate_create_cli(self):
        cli_text = const.BastionHost.CREATE_PREFIX
        if self.name:
            cli_text = cli_text + const.BastionHost.CreateCli.NAME.value + " " + self.name + " "
        if self.resource_group:
            cli_text = cli_text + const.BastionHost.CreateCli.RESOURCE_GROUP.value + " " + self.resource_group.name + " "
        if self.vnet:
            cli_text = cli_text + const.BastionHost.CreateCli.VNET.value + " " + self.vnet.name + " "
        if self.location:
            cli_text = cli_text + const.BastionHost.CreateCli.LOCATION.value + " " + self.location.name + " "
        return cli_text

    def save(self):
        self.resource_group = self.vnet.resource_group
        self.location = self.vnet.location
        self.create_cli_text = self.generate_create_cli()
        super(BastionHost, self).save()


class BastionSubnet(Subnet):
    sb_bastion = models.OneToOneField(BastionHost, on_delete=models.CASCADE, null=False)
    sn_address_space = models.CharField(max_length=100, verbose_name="AzureBastionSubnet address space")

    def save(self):
        self.vnet = self.sb_bastion.vnet
        self.name = const.Subnet.DefaultValue.BASTION_SUBNET_NAME.value
        self.subnet_address = self.sn_address_space
        self.resource_group = self.sb_bastion.resource_group
        super(BastionSubnet, self).save()


class BastionPublicIp(PublicIpAddress):
    pia_bastion = models.OneToOneField(BastionHost, on_delete=models.CASCADE, null=False)

    def save(self):
        self.resource_group = self.pia_bastion.resource_group
        super(BastionPublicIp, self).save()
        create_cli = CreateCli.objects.filter(resource_model_id=self.pia_bastion.id).get()
        create_cli.create_cli = create_cli.create_cli + " " + const.BastionHost.CreateCli.PUBLIC_IP.value + " " + self.name + " "
        create_cli.save()


class AzureFireWall(ResourceBase):
    vnet = models.OneToOneField(VirtualNetwork, on_delete=models.CASCADE, null=False)

    def generate_create_cli(self):
        cli_text = const.AzureFireWall.CREATE_PREFIX
        if self.name:
            cli_text = cli_text + const.BastionHost.CreateCli.NAME.value + " " + self.name + " "
        if self.resource_group:
            cli_text = cli_text + const.BastionHost.CreateCli.RESOURCE_GROUP.value + " " + self.resource_group.name + " "
        if self.vnet:
            cli_text = cli_text + const.BastionHost.CreateCli.VNET.value + " " + self.vnet.name + " "
        if self.location:
            cli_text = cli_text + const.BastionHost.CreateCli.LOCATION.value + " " + self.location.name + " "
        return cli_text

    def save(self):
        self.resource_group = self.vnet.resource_group
        self.location = self.vnet.location
        self.create_cli_text = self.generate_create_cli()
        super(AzureFireWall, self).save()


class FireWallSubnet(Subnet):
    sb_firewall = models.OneToOneField(AzureFireWall, on_delete=models.CASCADE, null=False)
    sn_address_space = models.CharField(max_length=100, verbose_name="AzureFirewallSubnet address space")

    def save(self):
        self.vnet = self.sb_firewall.vnet
        self.name = const.AzureFireWall.DefaultValue.FIREWALL_SUBNET_NAME.value
        self.subnet_address = self.sn_address_space
        self.resource_group = self.sb_firewall.resource_group
        super(FireWallSubnet, self).save()


class FireWallPublicIp(PublicIpAddress):
    pia_firewall = models.OneToOneField(AzureFireWall, on_delete=models.CASCADE, null=False)

    def save(self):
        self.resource_group = self.pia_firewall.resource_group
        super(FireWallPublicIp, self).save()
        create_cli = CreateCli.objects.filter(resource_model_id=self.pia_firewall.id).get()
        create_cli.create_cli = create_cli.create_cli + " " + const.AzureFireWall.CreateCli.PUBLIC_IP.value + " " + self.name + " "
        create_cli.save()


def create_az_cli(instance, created, **kwargs):
    if created:
        CreateCli.objects.create(resource_model=instance, create_cli=instance.create_cli_text)
        TestCli.objects.create(resource=instance, test_cli=instance.test_cli_text)
    else:
        create_cli = instance.createcli
        create_cli.create_cli = instance.create_cli_text
        create_cli.save()

        test_cli = instance.testcli
        test_cli.test_cli = instance.test_cli_text
        test_cli.save()


for subclass in AzureBaseModel.__subclasses__():
    post_save.connect(create_az_cli, sender=subclass)
    for sub in subclass.__subclasses__():
        post_save.connect(create_az_cli, sender=sub)
        for sub1 in sub.__subclasses__():
            post_save.connect(create_az_cli, sender=sub1)
