from django.contrib import admin
from nonrelated_inlines.admin import NonrelatedStackedInline
from .models import VirtualNetwork, Subnet, ResourceGroup, Location, Subscription, DdosProtectionPlan, BastionHost, \
    BastionSubnet, BastionPublicIp, AzureFireWall, FireWallSubnet, FireWallPublicIp

admin.site.register(Subscription)
admin.site.register(Location)


class ResourceGroupInline(admin.ModelAdmin):
    exclude = ('create_cli', 'test_cli')


class SubnetInline(admin.StackedInline):
    model = Subnet
    extra = 0
    fk_name = "vnet"
    fieldsets = [
        (None, {'fields': ['name', 'subnet_address', ]}),
    ]


class BastionInline(admin.StackedInline):
    model = BastionHost
    extra = 0
    fk_name = "vnet"
    exclude = ('resource_group', 'location')


class BastionSubnetInline(NonrelatedStackedInline):
    def get_form_queryset(self, obj):
        pass

    def save_new_instance(self, parent, instance):
        if parent.bastionhost:
            instance.sb_bastion = parent.bastionhost

    model = BastionSubnet
    extra = 0
    fk_name = "vnet"
    max_num = 1
    fieldsets = [
        (None, {'fields': ['sn_address_space']}),
    ]


class BastionPublicIpInline(NonrelatedStackedInline):
    def get_form_queryset(self, obj):
        pass

    def save_new_instance(self, parent, instance):
        if parent.bastionhost:
            instance.pia_bastion = parent.bastionhost

    model = BastionPublicIp
    extra = 0
    max_num = 1
    fieldsets = [
        (None, {'fields': ['name']}),
    ]


class FirewallInline(admin.StackedInline):
    model = AzureFireWall
    extra = 0
    fk_name = "vnet"
    exclude = ('resource_group', 'location')


class FirewallSubnetInline(NonrelatedStackedInline):
    def get_form_queryset(self, obj):
        pass

    def save_new_instance(self, parent, instance):
        if parent.azurefirewall:
            instance.sb_firewall = parent.azurefirewall

    model = FireWallSubnet
    extra = 0
    fk_name = "vnet"
    max_num = 1
    fieldsets = [
        (None, {'fields': ['sn_address_space']}),
    ]


class FirewallPublicIpInline(NonrelatedStackedInline):
    def get_form_queryset(self, obj):
        pass

    def save_new_instance(self, parent, instance):
        if parent.azurefirewall:
            instance.pia_firewall = parent.azurefirewall

    model = FireWallPublicIp
    extra = 0
    max_num = 1
    fieldsets = [
        (None, {'fields': ['name']}),
    ]


class VirtualNetworkAdmin(admin.ModelAdmin):
    inlines = [SubnetInline, BastionInline, BastionSubnetInline, BastionPublicIpInline, FirewallInline,
               FirewallSubnetInline, FirewallPublicIpInline]
    exclude = ('create_cli', 'test_cli')


class DDosProtectionPlanInline(admin.ModelAdmin):
    model = DdosProtectionPlan
    fieldsets = [
        (None, {'fields': ['resource_group', 'name', ]}),
    ]


admin.site.register(ResourceGroup, ResourceGroupInline)
admin.site.register(VirtualNetwork, VirtualNetworkAdmin)
admin.site.register(DdosProtectionPlan, DDosProtectionPlanInline)
