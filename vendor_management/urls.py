
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vendors.urls')),  # This should route 'api/' to the vendors app
]