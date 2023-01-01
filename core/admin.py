from django.contrib import admin
from django.utils.html import format_html
# * models
from core.models import Home

# Register your models here.

# * home admin


class HomeAdmin(admin.ModelAdmin):
    
    # * deactive add button
    def has_add_permission(self, request):
        return False
    
    # * deactive delete button
    def has_delete_permission(self, request, obj=None):
        return False
    

    # * image preview
    def image_preview(self, obj):
        return format_html('<img src="{}" width="200" />'.format(obj.image.url))
    image_preview.short_description = 'Imagen principal'

    # * brand image preview

    def brand_image_preview(self, obj):
        return format_html('<img src="{}" width="200" />'.format(obj.brand_image.url))

    brand_image_preview.short_description = 'Imagen de marca'

    # * list display
    list_display = ('title', 'image_preview', 'brand_image_preview')

    fieldsets = (
        ('Página principal', {
         'fields': ('title', 'subtitle', 'description', 'image', 'brand_image')}),
    )


# * admin
admin.site.register(Home, HomeAdmin)
