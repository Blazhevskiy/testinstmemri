from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Condo, CondoType, Address, Amenity, Group, Email, Phone, Organization


class AdminCondo(admin.ModelAdmin):
    list_display = ('condo_name', 'picture', 'description', 'amenity_link', 'building_type')

    def amenity_link(self, obj):
        if obj.amenities:
            return mark_safe(
                '<a href="/admin/condos/amenity/?q={0}">Amenities</a>'.format(obj.id)
            )

    amenity_link.description = 'Amenities'


class AdminEmail(admin.ModelAdmin):
    list_display = ('email', 'condo')


class AdminPhone(admin.ModelAdmin):
    list_display = ('phone_number', 'phone_number_canonical')


class AdminOrganization(admin.ModelAdmin):
    list_display = ('name', 'title', 'condo')


class AdminAmenity(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('condo__id',)


admin.site.register(Amenity, AdminAmenity)
admin.site.register(Email, AdminEmail)
admin.site.register(Phone, AdminPhone)
admin.site.register(Condo, AdminCondo)
admin.site.register(Organization, AdminOrganization)
