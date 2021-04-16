from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Shop

# Register your models here.


@admin.register(Shop)
class ShopAdmin(OSMGeoAdmin):
    default_lon = 1399219
    default_lat = 7496079
    default_zoom = 12
