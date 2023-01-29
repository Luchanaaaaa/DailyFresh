from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views
from .views import RegisterView

urlpatterns = [
    # path('register/', views.register, name = 'register'),
    # path('register_handle/', views.register_handle, name='register_handle'),
    path('register/', RegisterView.as_view(), name = 'register'),
]