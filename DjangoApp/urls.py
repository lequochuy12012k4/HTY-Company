from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^data/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
