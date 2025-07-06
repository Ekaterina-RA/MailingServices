from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('messaging.urls', namespace='messaging')),
    path('users/', include('users.urls', namespace='users')),
]