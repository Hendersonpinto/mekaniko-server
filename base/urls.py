from django.urls import path
from . import views

urlpatterns = [
    path("brands/", views.brandList, name="brand-list"),
    path("brands/<int:pk>", views.brandDetail, name="brand-detail"),
    path("car-models/", views.carModelList, name="car-model-list"),
    path("car-models/<int:pk>", views.carModelDetail, name="car-model-detail"),
    path("categories/", views.categoryList, name="category-list"),
    path("categories/<int:pk>", views.categoryDetail, name="category-detail"),
    path("services/", views.serviceList, name="service-list"),
    path("services/<int:pk>", views.serviceDetail, name="service-detail"),
]
