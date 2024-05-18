# incomes/urls.py

from django.urls import path
from .views import (
    income_list,
    income_detail,
    income_create,
    income_update,
    income_delete,
)

urlpatterns = [
    path('', income_list, name='income_list'),
    path('create/', income_create, name='income_create'),
    path('<int:income_id>/', income_detail, name='income_detail'), # dodat allocation amonts barchart with values for each pool
    path('<int:income_id>/update/', income_update, name='income_update'),
    path('<int:income_id>/delete/', income_delete, name='income_delete'),
]
