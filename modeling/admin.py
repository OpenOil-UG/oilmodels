from django.contrib import admin
from modeling.models import InformationType, DataSource, Reserve, Production, Cost, UnreviewedData
# Register your models here.


for table in (InformationType, DataSource, Reserve, Production, Cost, UnreviewedData):
    admin.site.register(table)




