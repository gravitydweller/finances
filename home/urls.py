from django.urls import path

from . import views
from .views import index, home_home
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home_home, name='home_home'),
]
