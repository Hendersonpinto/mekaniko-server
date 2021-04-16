from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models


class Shop(models.Model):
    name = models.CharField(max_length=120)
    location = models.PointField()
