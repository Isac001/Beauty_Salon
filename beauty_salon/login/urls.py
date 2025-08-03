# Django and project imports.
from django.urls import path
from . import views
from .services import logout_user 

# URL patterns for the login app.
urlpatterns = [

    # Maps the root URL ('/') to the LoginView.
    path('', views.LoginView.as_view(), name='login'),
    
    # Maps the 'logout/' URL to the logout function.
    path('logout/', logout_user, name='logout'),
]