# 
from django.conf.urls import include, url
from ooapi import views

v01_urlpatterns = [
    # Examples:
    url(r'^documentation/?', views.documentation, name="documentation"),
    url(r'^concessions/?', views.concessions, name="concessions"),
]

urlpatterns = [
    url(r'^v0.1/', include(v01_urlpatterns)),
    url(r'^/?', include(v01_urlpatterns)),
    ]
