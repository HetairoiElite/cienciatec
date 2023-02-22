from django.contrib import admin
from .models import School
from django.contrib import messages

# Register your models here.


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',  'is_external')
    fields = ('name', 'is_external')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = (
        'is_external',)

    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass

    def save_model(self, request, obj, form, change):
        if change:
            messages.success(
                request, 'La escuela se ha actualizado correctamente')
        else:
            messages.success(request, 'La escuela se ha creado correctamente')

        obj.save()

    def delete_model(self, request, obj):
        messages.success(request, 'La escuela se ha eliminado correctamente')
        obj.delete()

    # * delete action message
    def delete_queryset(self, request, queryset):
        messages.success(
            request, 'Las escuelas se han eliminado correctamente')
        queryset.delete()


admin.site.register(School, SchoolAdmin)
