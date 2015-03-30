# 
from django.conf.urls import include, url
from modeling import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oilmodels.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^sources/?', views.sources, name="sources"),
]
