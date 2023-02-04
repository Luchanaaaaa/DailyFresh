from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required
from .import views
from .views import RegisterView, LoginView, UserInfoView, UserOrderView, AddressView
app_name='user'

urlpatterns = [

    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('active/<token>/', RegisterView.as_view(), name = 'active'),

    path('', login_required(UserInfoView.as_view()), name='user'),
    path('order/', login_required( UserOrderView.as_view()), name='order'),
    path('address/', login_required(AddressView.as_view()), name='address'),

]