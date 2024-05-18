# pools/urls.py

from django.urls import path
from .views import (
    pool_home,
    pool_detail,
    pool_update,
    pool_transfer_create
)

urlpatterns = [
    path('home/', pool_home, name='pool_home'),
    path('<int:pool_id>/', pool_detail, name='pool_detail'),
    path('transfer/', pool_transfer_create, name='pool_transfer_create'),
    path('<int:pool_id>/update/', pool_update, name='pool_update'),  
]
