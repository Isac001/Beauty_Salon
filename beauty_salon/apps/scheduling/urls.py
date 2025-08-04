# Django imports.
from django.urls import path

# Local application imports.
from .views import *

# Define the name of the app
app_name = 'scheduling'

# URL patterns for the scheduling app.
urlpatterns = [

    # List Views
    path(
        '', 
        ScheduledAndCanceledListView.as_view(), 
        name='list-scheduled-canceled'
    ),
    path(
        'active/', 
        CompletedAndExecutingListView.as_view(), 
        name='list-completed-executing'
    ),
    path(
        'completed/', 
        CompletedOnlyListView.as_view(), 
        name='list-completed-only'
    ),
    
    # CUD Operations (Create, Update, "Delete")
    path(
        'create/', 
        SchedulingCreateView.as_view(), 
        name='scheduling-create'
    ),
    path(
        'update/<int:pk>/', 
        SchedulingUpdateView.as_view(), 
        name='scheduling-update'
    ),
    path(
        'cancel/<int:pk>/', 
        SchedulingCancelView.as_view(), 
        name='scheduling-cancel'
    ),
]