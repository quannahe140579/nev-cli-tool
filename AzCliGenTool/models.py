from abc import ABC
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import AzureCliFactory
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

    def save(self):
        super(AzureBaseModel, self).save()


class CreateCli(models.Model):
    create_cli = models.CharField(max_length=300, default="123")
    resource_model = models.OneToOneField(AzureBaseModel, on_delete=models.CASCADE)


class TestCli(models.Model):
    test_cli = models.CharField(max_length=300, default="123")
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


class VirtualNetwork(ResourceBase):
    address_space = models.CharField(max_length=100, blank=False, default="10.0.0.0/16")
    dns_server = models.CharField(max_length=100, blank=True)

    def generate_create_cli(self):
        cli_text = const.VirtualNetwork.CREATE_PREFIX
        # Code more here
        return cli_text

    def save(self):
        self.create_cli_text = self.generate_create_cli()
        super(VirtualNetwork, self).save()

    def __str__(self):
        return self.name


class Subnet(ResourceBase):
    vnet = models.ForeignKey(VirtualNetwork, on_delete=models.CASCADE, null=False)
    subnet_address = models.CharField(max_length=100, blank=False, default="10.0.0.0/24", unique=True,
                                      verbose_name="Subnet Address Space")

    def generate_create_cli(self):
        pass

    def save(self):
        super(Subnet, self).save()


# class PublicIpAddress(ResourceBase):
#     public_ip_name = models.CharField(max_length=100, blank=False, default="MySubnet", unique=True)
#
#
# class BastionHost(ResourceBase):
#     vnet = models.ForeignKey(VirtualNetwork, on_delete=models.CASCADE, null=False)
#
#
# class BastionPublicIp(PublicIpAddress):
#     bastion_host = models.OneToOneField(BastionHost, on_delete=True)


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
