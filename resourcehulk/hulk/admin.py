from django.contrib import admin
from hulk.models import (
    Company, Project, Statement,
    Search, SearchResult, SourceInfo)
#    Company, Concession, Document, Statement, Project,
#    Commodity, ConcessionAlias, CompanyAlias,
#    Search,SearchResult, SourceInfo)

for table in (Company, Project, Statement,
              Search, SearchResult, SourceInfo):
#              Concession, Document,Statement,Project,
#              Commodity, ConcessionAlias, CompanyAlias,
#              Search, SearchResult, SourceInfo):
    admin.site.register(table)

# Register your models here.
