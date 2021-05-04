from django.urls import path
from base.views import user_views as views
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path("", views.userList, name="user-list"),
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', views.registerUser,
         name='register-user'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile/", views.getUserProfile, name="users-profile"),
]
