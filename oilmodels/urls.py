from django.conf.urls import include, url
from django.contrib import admin
import modeling.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'oilmodels.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include(modeling.urls)),
]