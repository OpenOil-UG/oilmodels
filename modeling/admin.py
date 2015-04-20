from django.contrib import admin
from modeling.models import InformationType, DataSource, Reserve, Production
# Register your models here.

'''
class LevelInline(admin.TabularInline):
    model=ReserveLevel

class ReserveAdmin(admin.ModelAdmin):
    inlines = [LevelInline,]
'''
for table in (InformationType, DataSource, Reserve, Production):
    admin.site.register(table)

#admin.site.register(Reserve, ReserveAdmin)


