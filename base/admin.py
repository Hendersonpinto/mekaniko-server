from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *

# Register your models here.


@admin.register(Shop)
class ShopAdmin(OSMGeoAdmin):
    default_lon = 1399219
    default_lat = 7496079
    default_zoom = 12


admin.site.register(Booking)
admin.site.register(BookingService)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(Car)
