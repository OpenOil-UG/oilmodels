from django.contrib import admin
from ooapi.models import Concession, ConcessionSearchResult, APIKey

# Register your models here.
for table in (Concession, ConcessionSearchResult, APIKey):
    admin.site.register(table)
