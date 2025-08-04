# Django imports.
from django.urls import path

# Local application imports.
from .views import *


app_name = 'salon_service'


# URL patterns for the salon service app.
urlpatterns = [
    path('', SalonServiceListView.as_view(), name='list-salon-service'),
    path('create/', SalonServiceCreateView.as_view(), name='create-salon-service'),
    path('update/<int:pk>/', SalonServiceUpdateView.as_view(), name='update-salon-service'),
    path('delete/<int:pk>/', SalonServiceDeleteView.as_view(), name='delete-salon-service'),
]