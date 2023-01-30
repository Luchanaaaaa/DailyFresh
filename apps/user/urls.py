from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views
from .views import RegisterView, LoginView
app_name='user'

urlpatterns = [

    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('active/<token>/', RegisterView.as_view(), name = 'active'),
]