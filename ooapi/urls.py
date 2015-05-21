# 
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from ooapi import views

redir_to_docs = RedirectView.as_view(url='http://openoil.net/openoil-api/')

v01_urlpatterns = [
    url(r'^concession/search?', views.concessions, name="concessions"),
    url(r'^concession/(?P<countrycode>[^/]*)/(?P<identifier>.*)', views.concession, name="concession"),
    url(r'^apikey/generate/?', views.new_api_key, name="generate_api_key"),
    url(r'^/?', redir_to_docs),
    url(r'^documentation/?', redir_to_docs),
]

urlpatterns = [
    url(r'^v0.1/', include(v01_urlpatterns)),
    url(r'^/?', include(v01_urlpatterns)),
    ]
