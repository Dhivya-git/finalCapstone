from django.urls import path
from . import views

# Handles the request for ecommerce app
urlpatterns = [
    path('', views.index),
]