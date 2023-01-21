from django.contrib import admin
from django.urls import path, include
from . import views

# Url patterns for apps and root url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('personal/', include('personal.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('simplecv/', include('simplecv.urls')),
]
