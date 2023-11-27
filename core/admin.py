from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.urls import reverse
# ¨messages

from django.contrib import messages

# * models
from core.models import Home, ArticleTemplate, ReceptionLetter
from .forms import HomeChangeForm, ReceptionLetterForm
# Register your models here.


# * article template admin inline

class ArticleTemplateInline(admin.TabularInline):
    model = ArticleTemplate
    extra = 0

# * ReceptionLetterAdmin


class ReceptionLetterAdmin(admin.StackedInline):
    model = ReceptionLetter
    can_delete = False

    form = ReceptionLetterForm

    def secretary_firm_preview(self, obj):

        return format_html(
            '<img src="{}" width="50" />'.format(obj.secretary_firm.url)
        )

    secretary_firm_preview.short_description = 'Firma del secretario'

    def president_firm_preview(self, obj):
        return format_html(
            '<img src="{}" width="50" />'.format(obj.president_firm.url)
        )

    president_firm_preview.short_description = 'Firma del presidente'

    def seal_preview(self, obj):

        return format_html(
            '<img src="{}" width="150" />'.format(obj.seal.url)
        )

    seal_preview.short_description = 'Sello del departamento de investigacion'

    fieldsets = (
        (None, {
            'fields': ('template', 'current_number', 'seal_preview', 'seal')
        }),
        ('Secretario del comite arbitraje', {
            'fields': ('secretary', 'secretary_firm_preview', 'secretary_firm')
        }),
        ('Presidente del comite arbitraje', {
            'fields': ('president', 'president_firm_preview', 'president_firm')
        }),
    )

    readonly_fields = (
        'seal_preview', 'secretary_firm_preview', 'president_firm_preview')

# * ReportLetterAdmin
from .models import ReportLetter
class ReportLetterAdmin(admin.StackedInline):
    model = ReportLetter
    
    can_delete = False
    
    

# * home admin


class HomeAdmin(admin.ModelAdmin):

    # * inline
    inlines = [
        ArticleTemplateInline,
        ReceptionLetterAdmin,
        ReportLetterAdmin
    ]

    # * deactive add button
    def has_add_permission(self, request):
        # * if no super user
        if not request.user.is_superuser:
            return False

        # * if super user
        if Home.objects.count() >= 1:
            return False

        return True

    # * deactive delete button
    def has_delete_permission(self, request, obj=None):

        # * if no super user
        if not request.user.is_superuser:
            return False

        # * if super user
        if Home.objects.count() >= 1:
            return False

        return True

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
        try:
            publication = obj.publications.filter(current=True).first()
            # print(publication)
            # * get current publication change url
            change_url = reverse(
                'admin:Eventos_publication_change', args=[publication.id])
            # print(change_url)

            return format_html(
                '<a href="{}">{}</a>'.format(change_url, publication)
            )
        except:
            return 'No hay publicación actual'

        #  return format_html(
        #     '<a href="{}">{}</a>'.format(
        #         reverse('admin:events_publication_change', args=[obj.publications.filter(current=True).first().id])),
        #     obj.publications.filter(current=True).first()
        # )
    current_publication.short_description = 'Publicación actual'

    form = HomeChangeForm

    # * list display
    list_display = ('title', 'image_preview',
                    'brand_image_preview', 'favicon_preview', )

    fieldsets = (
        ('Información general', {
            'fields': (
                'title', 'subtitle', 'description',
                'image_previewc', 'image',
                'brand_image_previewc', 'brand_image',
                'favicon_previewc', 'favicon',
                'current_publication',
                # 'publication'
            )
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

    def message_user(self, *args, **kwargs):
        pass

    def save_model(self, request, obj, form, change):
        if change:
            messages.add_message(
                request, messages.SUCCESS, 'Se ha actualizado la información de la página principal.')

        super().save_model(request, obj, form, change)


# * admin
admin.site.register(Home, HomeAdmin)


from django.contrib import admin
# from cabinet.admin import FileAdmin
# from cabinet.models import File
from django.utils.formats import date_format
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

# Register your models here.


# class CustomFileAdmin(FileAdmin):

#     @admin.display(description='Detalles')
#     def admin_details(self, instance):
#         details = [
#             instance.caption,
#             instance.copyright,
#             _("Creado en %(created_at)s, ultima modificación %(updated_at)s")
#             % {
#                 "created_at": date_format(instance.created_at, "SHORT_DATE_FORMAT"),
#                 "updated_at": date_format(instance.updated_at, "SHORT_DATE_FORMAT"),
#             },
#         ]
#         return format_html(
#             "<small>{}</small>",
#             format_html_join(mark_safe("<br>"), "{}", ((d,)
#                              for d in details if d)),
#         )
        
#     admin_details.short_description = "Detalles"
    
#     def admin_file_name(self, instance):
#         return format_html(
#             "{} <small>({})</small>",
#             instance.file_name,
#             filesizeformat(instance.file_size),
#         )
        
#     admin_file_name.short_description = "Nombre del archivo"

# # * Unregister the default FileAdmin
# admin.site.unregister(File)

# * Register the custom FileAdmin
# admin.site.register(File, CustomFileAdmin)