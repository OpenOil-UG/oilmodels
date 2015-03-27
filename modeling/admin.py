from django.contrib import admin
from modeling.models import InformationType, DataSource
# Register your models here.

for table in (InformationType, DataSource):
    admin.site.register(table)


