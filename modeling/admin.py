from django.contrib import admin
from modeling.models import InformationType, DataSource, Reserve, Production, Cost
# Register your models here.


for table in (InformationType, DataSource, Reserve, Production, Cost):
    admin.site.register(table)




