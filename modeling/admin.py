from django.contrib import admin
from modeling.models import InformationType, DataSource, Reserve
# Register your models here.

for table in (InformationType, DataSource, Reserve):
    admin.site.register(table)


