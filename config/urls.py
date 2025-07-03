from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from messaging.views import MessagingHomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('messaging/', include('messaging.urls', namespace='messaging')),
    path('', MessagingHomeView.as_view(), name='home'),
]

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)