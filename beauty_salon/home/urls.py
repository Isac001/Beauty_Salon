# home/urls.py
from django.urls import path
from .views import *

app_name = 'home' # Define o nome da aplicação para usar nas URLs

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]