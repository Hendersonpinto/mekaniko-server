"""mekaniko URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# This way I can use the variables defined in my settings.py
from django.conf import settings

# This is a built-in function that enables the connection between our url defined by MEDIA_URL and the static folder we want to deliver from MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.urls'))
]

# This way we are defining the URL used to render images in the browser and the folder where those images are stored.
# The built-in static function will make the connection and handle the delivery.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
