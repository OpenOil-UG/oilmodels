# 
from django.conf.urls import include, url
from modeling import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oilmodels.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^info_types/?', views.infotypes, name="info_types"),
    url(r'^data_sources/?', views.datasources, name="data_sources"),
    url(r'^reserves/?', views.reserves, name="reserves"),
    url(r'^production/??', views.production, name="production"),
    url(r'^add/csv??', views.import_csv, name="import_csv"),
]
