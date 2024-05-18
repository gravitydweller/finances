# incomes/urls.py

from django.urls import path
from .views import (
    income_home,
    income_detail,
    income_create,
    income_update,
    income_delete,
)

urlpatterns = [
    path('home/', income_home, name='income_home'),  # URL for the income homepage
    path('create/', income_create, name='income_create'),
    path('<int:income_id>/', income_detail, name='income_detail'),
    path('<int:income_id>/update/', income_update, name='income_update'),
    path('<int:income_id>/delete/', income_delete, name='income_delete'),
]
