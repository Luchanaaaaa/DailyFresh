from django.urls import path
from .import views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('register_handle', views.register_handle, name='register_handle'),

]