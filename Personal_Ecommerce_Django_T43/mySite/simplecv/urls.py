from django.urls import path
from . import views

# Handles the request for simplecv app
urlpatterns = [
    path('', views.index),
]