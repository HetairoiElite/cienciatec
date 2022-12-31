from django.contrib import admin
from .models import School

# Register your models here.


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'zip_code', 'country',
                    'phone', 'email', 'website', 'is_external', 'created_at', 'updated_at')
    search_fields = ('name', 'address', 'city', 'state', 'zip_code',
                     'country', 'phone', 'email', 'website', 'created_at', 'updated_at')
    list_filter = ('city', 'state', 'country',
                   'is_external', 'created_at', 'updated_at')


admin.site.register(School, SchoolAdmin)
