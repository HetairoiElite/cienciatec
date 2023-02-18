from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from .models import *

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


# @admin.action(description='Enviar dictamen de arbitraje')
# def send_arbitration_report(modeladmin, request, queryset):
#     try:
#         # * check if queryset has none approved articles

#         if queryset.filter(is_approved=None).exists():
#             raise Exception('Tiene artículos sin dictaminar')

#         for article in queryset:
#             article.send_arbitration_report()


#         modeladmin.message_user(request, 'Se han enviado los dictámenes de arbitraje', level=messages.SUCCESS)

#     except Exception as e:
#         modeladmin.message_user(request, str(e), level=messages.ERROR)

@admin.action(description='Enviar carta de recepción')
def send_reception_letter(modeladmin, request, queryset):
    try:
        # * check if queryset has none approved articles

        if queryset.filter(status='1').exists():
            raise Exception(
                'Hay artículos sin recibir. Marque como recibido antes de enviar la carta de recepción')

        for article in queryset:
            article.send_reception_letter()

        messages.success(
            request, 'Se han enviado las cartas de recepción')

    except Exception as e:
        messages.error(request, str(e))


@admin.action(description='Marcar como recibido')
def mark_as_received(modeladmin, request, queryset):
    # from .tasks import go_to_sleep
    # go_to_sleep.delay(10)
    # * add context to view
    queryset.update(status='2')
    messages.success(request, 'Se han marcado como recibidos')


class ArticleProposalAdmin(admin.ModelAdmin):

    # actions = [send_arbitration_report]
    actions = [mark_as_received, send_reception_letter]

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

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if not request.user.is_superuser:

            context.update({
                'show_save': True,
                'show_save_and_continue': False,
                'show_save_and_add_another': False,
                'show_delete': False
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ('title', 'author_link', 'template', 'new_school', 'status')
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
        ('proposal_reception__publication__numero_publicacion'),
        # ('is_approved')
    )

    fieldsets = (
        (None, {'fields': ('proposal_reception', 'title',
         'author_link', 'modality', 'school', 'template', 'status')},),
    )

    readonly_fields = ('proposal_reception', 'title',
                       'author_link', 'modality', 'school', 'template', )

    def message_user(self, request, message, level):
        pass

    def save_model(self, request, obj, form, change):
        if change:

            # * translate message

            messages.add_message(request, messages.SUCCESS,
                                 format_html(f'La propuesta de artículo <a href="/admin/proposal_reception/articleproposal/{obj.id}">{obj.title}</a> ha sido actualizada correctamente.'))

        super().save_model(request, obj, form, change)
    # * change_list_context


admin.site.register(ArticleProposal, ArticleProposalAdmin)
