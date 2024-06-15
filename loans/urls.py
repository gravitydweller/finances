# loans/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.loans_home, name='loan_home'),
]