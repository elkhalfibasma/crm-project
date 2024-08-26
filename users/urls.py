# In users/urls.py
from django.urls import path
from .views import register_view, login_view, custom_logout

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
]
