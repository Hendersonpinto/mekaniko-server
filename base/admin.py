from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *
from django.contrib.auth.models import Group


# Customizing our admin interface
admin.site.unregister(Group)
admin.site.site_header = "Mekaniko Admin"


@admin.register(Shop)
class ShopAdmin(OSMGeoAdmin):
    default_lon = 1399219
    default_lat = 7496079
    default_zoom = 12


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo']
    search_fields = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Note: We can't pass m2m relationships in the list display!
    list_display = ['id', 'name', 'icon', 'price']
    search_fields = ['name']
    # Handy UI for when we ened to establish a m2m relationship
    filter_horizontal = ['categories']
    # This defines a very useful filter to the right side of the admin interface
    list_filter = ['categories']


admin.site.register(Booking)
admin.site.register(BookingService)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(CarModel)
admin.site.register(Car)
