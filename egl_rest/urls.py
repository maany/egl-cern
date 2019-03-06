from django.urls import path

from . import views

urlpatterns = [
    path('sites', views.index, name='index'),
]