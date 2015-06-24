from django.contrib import admin
from modeling.models import InformationType, DataSource, Reserve, Production, Cost, ExtractedData, ExtraInformation
# Register your models here.

from auditlog.models import LogEntry
admin.site.register(LogEntry)

for table in (InformationType, DataSource, Reserve, Production, Cost, ExtractedData, ExtraInformation):
    admin.site.register(table)




