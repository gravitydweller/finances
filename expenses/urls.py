# expenses/urls.py

from django.urls import path
from .views import (
    expense_home,
    expense_detail,
    expense_create,
    expense_update,
    expense_delete,
)

urlpatterns = [
    path('home/', expense_home, name='expense_home'),  # URL for the expense homepage
    path('create/', expense_create, name='expense_create'),
    path('<int:expense_id>/', expense_detail, name='expense_detail'),
    path('<int:expense_id>/update/', expense_update, name='expense_update'),
    path('<int:expense_id>/delete/', expense_delete, name='expense_delete'),
]
