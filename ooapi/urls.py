# 
from django.conf.urls import include, url
from ooapi import views

urlpatterns = [
    # Examples:
    url(r'^documentation/?', views.documentation, name="documentation"),
    url(r'^concessions/?', views.concessions, name="concessions"),
]
