from django.urls import path
from . import views

urlpatterns = [
    path('sites', views.sites, name='sites'),
    path('sites/<int:site_id>', views.site, name='site'),
    path('vos', views.vos, name='vos'),
    path('vos/<int:vo_id>', views.vo, name='vo'),
    path('federations', views.federations, name='federations'),
    path('federations/<int:federation_id>', views.federation, name='federation'),
    path('data_links', views.data_links, name='data_links'),
    path('raw_data_links', views.raw_data_links, name='data_links'),
    path('countries', views.countries, name='countries'),
]
