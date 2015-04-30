from django.contrib import admin
from ooapi.models import Concession, ConcessionSearchResult

# Register your models here.
for table in (Concession, ConcessionSearchResult):
    admin.site.register(table)
