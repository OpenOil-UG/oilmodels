# 
from django.conf.urls import include, url
from modeling import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oilmodels.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/?$', views.dataindex, name='dataindex'),
    url(r'^info_types/?', views.infotypes, name="info_types"),
    url(r'^data_sources/?', views.datasources, name="data_sources"),
    url(r'^reserves/?', views.reserves, name="reserves"),
    url(r'^production/?', views.production, name="production"),
    url(r'^costs/?', views.costs, name="costs"),
    url(r'^add/csv/?', views.import_csv, name="import_csv"),
    url(r'^add/manual/?', views.import_manual, name="import_manual"),
    url(r'^add/json/?', views.import_json, name="import_json"),
    url(r'^add/pdf/?', views.import_pdf, name="import_pdf"),
]
