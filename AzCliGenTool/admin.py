from django.contrib import admin
from nonrelated_inlines.admin import NonrelatedStackedInline
from .models import VirtualNetwork, Subnet, ResourceGroup, Location, Subscription

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

    def save_new(self, form, commit=True):
        pass


class VirtualNetworkAdmin(admin.ModelAdmin):
    inlines = [SubnetInline]
    exclude = ('create_cli', 'test_cli')


admin.site.register(ResourceGroup, ResourceGroupInline)
admin.site.register(VirtualNetwork, VirtualNetworkAdmin)
