# loans/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.loans_home, name='loan_home'),
    path('create/', views.create_loan, name='loan_create'),  # Example URL for creating a loan
    # Add more URLs as needed
]