from .forms import ArticleProposalAdminForm
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from .models import *
from apps.reviewer_assignment.models import *
# * user
from apps.registration.models import Profile

# * jet filters
from jet.filters import RelatedFieldAjaxListFilter


# Register your models here.


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1
    max_num = 3

    fields = ('image', )

    readonly_fields = ('image',)

    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class CoauthorInline(admin.TabularInline):
    model = Coauthor
    extra = 1

    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'email')

    readonly_fields = ('nombre', 'email',
                       'apellido_paterno', 'apellido_materno')


# @admin.action(description='Enviar carta de recepción')
# def send_reception_letter(modeladmin, request, queryset):


@admin.action(description='Marcar como recibido')
def mark_as_received(modeladmin, request, queryset):
    from dotenv import load_dotenv
    import os
    from django.conf import settings
    # Asegúrate de importar NamedTemporaryFile desde tempfile
    from tempfile import NamedTemporaryFile

    load_dotenv()

    DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

    if DJANGO_SETTINGS_MODULE == 'cienciatec.settings.prod':
        # Asegúrate de importar el modelo Home desde tu aplicación
        from core.models import Home
        from django.core.files.storage import default_storage

        home = Home.objects.first()
        template = home.reception_letters.template.path
        secretary_firm = home.reception_letters.secretary_firm.path
        president_firm = home.reception_letters.president_firm.path
        seal = home.reception_letters.seal.path

        # Crear archivos temporales para cada archivo
        temp_template = NamedTemporaryFile(delete=False)
        temp_secretary_firm = NamedTemporaryFile(delete=False)
        temp_president_firm = NamedTemporaryFile(delete=False)
        temp_seal = NamedTemporaryFile(delete=False)

        # Guardar cada archivo en su respectivo archivo temporal
        with default_storage.open(template) as f:
            with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename(template)), 'wb') as d:
                d.write(f.read())

        with default_storage.open(secretary_firm) as f:
            with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename(secretary_firm)), 'wb') as d:
                d.write(f.read())

        with default_storage.open(president_firm) as f:
            with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename(president_firm)), 'wb') as d:
                d.write(f.read())

        with default_storage.open(seal) as f:
            with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename(seal)), 'wb') as d:
                d.write(f.read())
        # from .tasks import go_to_sleep
        # go_to_sleep.delay(10)
        # * add context to view

    for article in queryset:
        # * create assignment and profile for each article

        Assignment.objects.get_or_create(
            article=article,
            publication=article.publication,
        )

    try:
        # * check if queryset has none approved articles
        for article in queryset:
            if article.status < '2':
                article.send_reception_letter()
                article.generate_template_as_pdf()

        # messages.success(
            # request, 'Se han enviado las cartas de recepción')
        queryset.update(status='2')

        messages.success(request, 'Se han marcado como recibidos')

    except Exception as e:
        messages.error(request, str(e))


@admin.action(description='Enviar dictamen')
def send_arbitration_report(modeladmin, request, queryset):
    # * si en el queryset hay artículos que ya tienen documento de dictamen no enviar

    for article in queryset:
        if article.dictamen_letter:
            messages.error(request, 'Algunos artículos ya tienen dictamen')
            return

        if article.status != '7' and article.status != '8':
            messages.error(
                request, 'Algunos artículos no están en dictamen o no han sido aceptados o rechazados')
            return

    for article in queryset:
        article.send_arbitration_report()


class ArticleProposalAdmin(admin.ModelAdmin):

    change_list_template = "admin/proposal_reception/change_list.html"

    form = ArticleProposalAdminForm

    # actions = [send_arbitration_report]
    actions = [mark_as_received, send_arbitration_report]

    def has_add_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False

        return True

    def author_link(self, obj):
        if obj.author is not None:
            return format_html(f'<a href="/admin/auth/user/{obj.author.id}">{obj.author}</a>')

    author_link.short_description = "Autor"

    # * arbitraje link list display

    def assignment_link(self, obj):

        if obj.status != '1':

            # * sin arbitraje
            if obj.status == '2':

                return format_html(f'<a href="/admin/Asignacion_Arbitros/assignment/{obj.assignment.id}">' +
                                   '<i class="fi fi-flag"></i> Asignar</a>'
                                   + '</a>')
            else:
                return format_html(f'<a href="/admin/Asignacion_Arbitros/assignment/{obj.assignment.id}">' +
                                   '<i class="fi fi-eye"></i> Ver asignación</a>'
                                   + '</a>')

        # * marcar como recibido
        print("HOLA")
        return format_html(f'Necesita ser recibido')

    assignment_link.short_description = "Seguimiento"

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if not request.user.is_superuser:

            context.update({
                'show_save': True,
                'show_save_and_continue': False,
                'show_save_and_add_another': False,
                'show_delete': False
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def download_template(self, obj):
        return format_html(f'<a href="{obj.template.url}"><i class="fi fi-download"></i> Descargar</a>')

    download_template.short_description = "Plantilla"

    list_display = ('title',
                    'assignment_link',
                    'author_link',
                    'download_template',
                    # 'new_school',
                    'status')
    search_fields = ('title', 'author__user__username',
                     'author__user__first_name', 'author__user__last_name')

    inlines = [
        ArticleImageInline,
        CoauthorInline,
    ]

    # * jet filters
    list_filter = (
        ('school', RelatedFieldAjaxListFilter),
        ('modality'),
        ('status'),
        ('publication__numero_publicacion'),
        # ('is_approved')
    )

    fieldsets = (
        (None, {'fields': ('publication', 'title',
         'author_link', 'modality', 'school', 'new_school', 'template', 'status', 'profiles',
                           'rights_transfer_letter')},),
    )

    readonly_fields = ('publication', 'title',
                       'author_link', 'modality', 'school', 'new_school', 'template', 'rights_transfer_letter')

    def get_readonly_fields(self, request, obj=None):
        # * si el estado es "en dictamen" (6) agregar retirar status de readonly
        if obj is not None:
            if obj.status != '6':
                return ('publication', 'title',
                        'author_link', 'modality', 'school', 'new_school', 'template', 'rights_transfer_letter', 'status')
            else:
                return ('publication', 'title',
                        'author_link', 'modality', 'school', 'new_school', 'template', 'rights_transfer_letter')

    def message_user(self, request, message, level):
        pass

    def save_model(self, request, obj, form, change):
        if change:

            if obj.status == '2':
                # * create assignment and profile for each article

                Assignment.objects.get_or_create(
                    article=obj,
                    publication=obj.publication,
                )

            # * translate message

            messages.add_message(request, messages.SUCCESS,
                                 format_html(f'La propuesta de artículo <a href="/admin/proposal_reception/articleproposal/{obj.id}">{obj.title}</a> ha sido actualizada correctamente.'))

        super().save_model(request, obj, form, change)
    # * change_list_context


admin.site.register(ArticleProposal, ArticleProposalAdmin)
