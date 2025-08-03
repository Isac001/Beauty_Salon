# Django imports.
from django.urls import path

# Local application imports.
from .views import *

# URL patterns for the client app.
urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('create/', ClientCreateView.as_view(), name='client-create'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),
]