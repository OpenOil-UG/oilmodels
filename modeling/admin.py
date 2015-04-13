from django.contrib import admin
from modeling.models import InformationType, DataSource, Reserve, ReserveLevel
# Register your models here.

class LevelInline(admin.TabularInline):
    model=ReserveLevel

class ReserveAdmin(admin.ModelAdmin):
    inlines = [LevelInline,]

for table in (InformationType, DataSource, ReserveLevel):
    admin.site.register(table)

admin.site.register(Reserve, ReserveAdmin)


