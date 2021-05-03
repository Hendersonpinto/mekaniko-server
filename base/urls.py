from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("users/profile/", views.getUserProfile, name="users-profile"),
    path("users/", views.userList, name="user-list"),
    path("brands/", views.brandList, name="brand-list"),
    path("brands/<int:pk>", views.brandDetail, name="brand-detail"),
    path("car-models/", views.carModelList, name="car-model-list"),
    path("car-models/<int:pk>", views.carModelDetail, name="car-model-detail"),
    path("categories/", views.categoryList, name="category-list"),
    path("categories/<int:pk>", views.categoryDetail, name="category-detail"),
    path("services/", views.serviceList, name="service-list"),
    path("services/<int:pk>", views.serviceDetail, name="service-detail"),
]
