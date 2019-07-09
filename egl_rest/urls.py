from django.urls import path
from . import views

urlpatterns = [
    path('sites', views.sites, name='sites'),
    path('sites/<int:site_id>', views.site, name='site'),
    path('data_links', views.data_links, name='data_links'),
]
