# core/urls.py

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path("admin/", admin.site.urls),
    path("", include('admin_black.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path("incomes/", include('incomes.urls')),
    path("pools/", include('pools.urls')),
    path('expenses/', include('expenses.urls')),
    path('loans/', include('loans.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)