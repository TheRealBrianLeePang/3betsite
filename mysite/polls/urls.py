from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^callback$', view=views.callback, name='callback'),
    path('', views.index, name='index'),
]

