from django.urls import path
from . import views

urlpatterns = [
    path('sites', views.sites, name='sites'),
    path('data_links', views.data_links, name='data_links'),
]
