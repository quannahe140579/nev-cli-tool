from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=100, blank=False, default="MySubscription")
    subscription_id = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name


def delete_resource_cli(self):
    CreateCli.objects.filter(pk=self.id).delete()
    TestCli.objects.filter(pk=self.id).delete()


class AzureBaseModel(models.Model):
    def save(self, create_cli_text, test_cli_text):
        super(AzureBaseModel, self).save()

    def delete(self):
        super(AzureBaseModel, self).delete()


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

    def __str__(self):
        return self.name

    def save(self):
        super(ResourceGroup, self).save("asd", "f")


class ResourceBase(AzureBaseModel):
    resource_group = models.ForeignKey(ResourceGroup, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=100, blank=False)


class VirtualNetwork(ResourceBase):
    address_space = models.CharField(max_length=100, blank=False, default="10.0.0.0/16")

    def save(self):
        super(VirtualNetwork, self).save()

    def __str__(self):
        return self.name


class Subnet(ResourceBase):
    vnet = models.ForeignKey(VirtualNetwork, on_delete=models.CASCADE, null=False)
    subnet_address = models.CharField(max_length=100, blank=False, default="10.0.0.0/24", unique=True,
                                      verbose_name="Subnet Address Space")

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
