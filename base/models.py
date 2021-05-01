from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator


class Shop(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='shops')
    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    location = models.PointField()
    open_time = models.TimeField('Open time', null=True, blank=True)
    close_time = models.TimeField('Close time', null=True, blank=True)
    wifi = models.BooleanField(default=False)
    physical_store = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    postal_code = models.CharField(
        "Postal Code", max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='bookings')
    shop = models.ForeignKey(
        Shop, on_delete=models.SET_NULL, null=True, related_name='bookings')
    # Since our intermediary table is a custom, we need to specify the through property
    # The through_fields accepts a tuple. First argument is how the model in which the m2m rel exist is named in the intermediary table
    # and the second argument is how the linked model is specified in the intermediary table
    # NOTE: We actually don't need the through_fields because Django can handle it by making assumptions but we can also be explicit
    services = models.ManyToManyField(
        'Service', through='BookingService', through_fields=('booking', 'service'))
    date = models.TimeField('Booking date', null=True, blank=True)
    # max_digits also counts the decimal places so to represent 99999.44 we would need max_digits=7
    total_price = models.DecimalField(
        'Total price', max_digits=14, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)


class BookingService(models.Model):
    # I need to enclose 'Service' with single quotes because the model is created after.
    service = models.ForeignKey(
        'Service', on_delete=models.SET_NULL, null=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    message = models.TextField(null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)


class Service(models.Model):
    # Note: we don't need to specify the m2m relationship with Booking because it already exists on the Booking model

    # Note 1: We don't need to create a custom intermediary table with Category because we are not adding any extra information on it
    # Note 2: We are defining the m2m relationship here because it's more likely to choose a category while creating the service than the other way around
    # Note 3: Since the m2m field is defined here, we don't need to define it in the Category model
    # Note 4: I need to wrap 'Service' with single quotes because the model is created after.
    categories = models.ManyToManyField('Category')
    name = models.CharField(max_length=100, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    # Since the m2m field is defined in the Service model, we don't need to define it here
    name = models.CharField(max_length=80, null=False, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return str(self.rating)


class Brand(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class CarModel(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return str(self.name)


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    car_model = models.ForeignKey(
        CarModel, on_delete=models.SET_NULL, null=True)
    year = models.PositiveIntegerField(
        default=2000, validators=[MinValueValidator(1900)])
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.car_model)
