# 
from django.conf.urls import include, url
from ooapi import views

urlpatterns = [
    # Examples:
    url(r'^concessions/?', views.concessions, name="concessions"),
]
