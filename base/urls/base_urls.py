from django.urls import path
from base.views import base_views as views
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path("shops/create/", views.shopCreate, name="shop-create"),
    path("shops/", views.shopListCreate, name="shop-list"),
    path("shops/<int:pk>", views.shopDetail, name="shop-detail"),
    path("brands/", views.brandList, name="brand-list"),
    path("brands/create/", views.brandCreate, name="brand-create"),
    path("brands/<int:pk>", views.brandDetail, name="brand-detail"),
    path("car-models/", views.carModelList, name="car-model-list"),
    path("car-models/<int:pk>", views.carModelDetail, name="car-model-detail"),
    path("categories/", views.categoryList, name="category-list"),
    path("categories/<int:pk>", views.categoryDetail, name="category-detail"),
    path("services/", views.serviceList, name="service-list"),
    path("services/<int:pk>", views.serviceDetail, name="service-detail"),
]
