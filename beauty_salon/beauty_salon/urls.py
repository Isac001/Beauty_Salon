# Django and project imports.
from django.contrib import admin
from django.urls import path, include 

# URL patterns
urlpatterns = [

    # Django URLs.
    path('admin/', admin.site.urls),

    # App's URLs.
    path('client/', include('client.urls')),
    path('salon_service/', include('salon_service.urls')),

    # Login URLs.
    path('', include('login.urls'))
]