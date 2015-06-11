from django.contrib import admin
from modeling.models import InformationType, DataSource, Reserve, Production, Cost, ExtractedData
# Register your models here.


for table in (InformationType, DataSource, Reserve, Production, Cost, ExtractedData):
    admin.site.register(table)




