from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.urls import reverse

# * models
from core.models import Home
from .forms import HomeChangeForm
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

    def image_previewc(self, obj):
        return format_html(
            '<img src="{}" width="200" /><a href="{}" target="_blank">{}</a>'.format(obj.image.url, obj.image.url, obj.image.url))

    image_previewc.short_description = 'Imagen principal'

    def image_preview(self, obj):
        return format_html(
            '<img src="{}" width="200" />'.format(obj.image.url)
        )

    image_preview.short_description = 'Imagen principal'

    # * brand image preview

    def brand_image_previewc(self, obj):
        return format_html(
            '<img src="{}" width="200" /><a href="{}" target="_blank">{}</a>'.format(
                obj.brand_image.url, obj.brand_image.url, obj.brand_image.url)
        )

    brand_image_previewc.short_description = 'Imagen de marca'

    def brand_image_preview(self, obj):
        return format_html(
            '<img src="{}" width="200" />'.format(obj.brand_image.url)
        )

    brand_image_preview.short_description = 'Imagen de marca'

    # * favicon preview

    def favicon_previewc(self, obj):
        return format_html(
            '<img src="{}" width="50" /><a href="{}" target="_blank">{}</a>'.format(
                obj.favicon.url, obj.favicon.url, obj.favicon.url)
        )

    favicon_previewc.short_description = 'Favicon'

    def favicon_preview(self, obj):
        return format_html(
            '<img src="{}" width="50" />'.format(obj.favicon.url)
        )

    favicon_preview.short_description = 'Favicon'

    def current_publication(self, obj):
        publication = obj.publications.filter(current=True).first()
        print(publication)
        # * get current publication change url
        change_url = reverse(
            'admin:events_publication_change', args=[publication.id])
        print(change_url)

        return format_html(
            '<a href="{}">{}</a>'.format(change_url, publication)
        )

        #  return format_html(
        #     '<a href="{}">{}</a>'.format(
        #         reverse('admin:events_publication_change', args=[obj.publications.filter(current=True).first().id])),
        #     obj.publications.filter(current=True).first()
        # )
    current_publication.short_description = 'Publicación actual'

    form = HomeChangeForm

    # * list display
    list_display = ('title', 'image_preview',
                    'brand_image_preview', 'favicon_preview', 'current_publication')

    fieldsets = (
        ('Información general', {
            'fields': (
                'title', 'subtitle', 'description',
                'image_previewc', 'image',
                'brand_image_previewc', 'brand_image',
                'favicon_previewc', 'favicon',
                'current_publication', 'publication')
        }),
        ('Archivos adjuntos', {
            'fields': (
                'convocatoria',

            )
        }),
        # ('Periodo de publicación', {'fields': ('publication',)})
    )

    readonly_fields = ('image_previewc', 'brand_image_previewc',
                       'favicon_previewc', 'current_publication')

    # radio_fields = {
    #     'publication': admin.VERTICAL,
    # }


# * admin
admin.site.register(Home, HomeAdmin)
