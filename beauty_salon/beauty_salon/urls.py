# Django and project imports.
from django.contrib import admin
from django.urls import path, include 

app_name = 'client'

# URL patterns
urlpatterns = [

    # Django URLs.
    path('admin/', admin.site.urls),

    # App's URLs.
    path('client/', include('apps.client.urls',)),
    path('salon_service/', include('apps.salon_service.urls')),
    path('employee/', include('apps.employee.urls')),
    path('scheduling/', include('apps.scheduling.urls')),

    # Login URLs.
    # path('', include('login.urls'))
    path('', include('home.urls')),
    
]