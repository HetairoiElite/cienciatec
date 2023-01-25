from django.contrib import admin
from .models import School

# Register your models here.


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',  'is_external')
    fields = ('name', 'is_external')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = (
        'is_external',)
    


admin.site.register(School, SchoolAdmin)
