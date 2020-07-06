# coding:utf-8

from django.conf.urls import url, include
from . import views

urlpatterns = [
               url(r'^callback/', views.main_callback),
                url(r'^data/', views.data),
                url(r'^order/', views.order),

               ]
