from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.db.models import Q
# Register your models here.

from jet import admin as jet_admin

from .models import *
from .forms import AssignmentForm

from apps.article_review.models import Review, Note


class ReviewInline(jet_admin.CompactInline):

    def get_notes(self, obj):

        # return format_html('<ul>' + '\n'.join(

        #     ['<li>Línea\t' + str(nota.line) + ': ' + str(nota) + '</li>'
        #      for nota in Note.objects.filter(
        #         review=obj
        #     )
        #     ]) + '</ul>')
        # * table foundation zurb

        return format_html(
            '<table class="hover"><thead><tr><th>Línea</th><th>Nota</th><th>¿Corrigió?</th></tr></thead>'
            + '\n'.join(
                ['<tr><td>\t' + str(nota.line) + '</td><td>' + str(nota) + '</td><td>\t' +
                 ('<img src="/static/admin/img/icon-yes.svg" alt="True">' if nota.value
                  else '<img src="/static/admin/img/icon-no.svg" alt="False">')
                 + '</td></tr>'
                 for nota in Note.objects.filter(
                    review=obj
                )
                ]
            ) + '</table>')

    get_notes.short_description = format_html(
        """<i class="fi-clipboard-notes"
        style="color:gray"> </i>Notas""")

    # * can't add
    def has_add_permission(self, request, obj=None):
        return False

    model = Review
    fk_name = 'assignment'
    can_delete = False
    extra = 0

    fields = (
        'referee',
        'get_notes',
        'comments',
        'enviado',
        'dictamen',
    )

    readonly_fields = (
        'referee',
        'get_notes',
        'comments',
        # 'enviado',
        'dictamen',
    )


class AssignmentAdmin(admin.ModelAdmin):

    inlines = [
        ReviewInline
    ]

    form = AssignmentForm

    def get_referees(self, obj):
        return format_html('\n'.join(

            ['<a href="/admin/auth/user/' + str(p.id) + '/change/#/tab/inline_0/"><i class="fi-torso"></i> ' +
             p.user.get_full_name() + '</a><br>' for p in obj.referees.all()]))
    get_referees.short_description = 'Árbitros'

    def get_profiles(self, obj):
        return format_html('<br>'.join(
            ['<a href="/admin/Asignacion_Arbitros/profile/' + str(p.id) + '/change/">' + str(p) + '</a>' for p in obj.article.profile.profiles.all()]))

    get_profiles.short_description = 'Perfiles'

    list_display = ('article', 'get_referees', 'status')

    readonly_fields = ('article', 'publication', 'get_profiles')

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        else:
            if obj.status != '1':
                return ('article', 'publication', 'get_profiles', 'get_referees',
                        # 'completed'
                        )
            else:
                return self.readonly_fields

    def get_fields(self, request, obj=None):
        if obj is None:
            return self.fields
        else:
            if obj.status != '1':
                return ('article', 'publication', 'get_profiles', 'get_referees', 'completed')

        return super().get_fields(request, obj)

    list_filter = ('status',)

    search_fields = ('article__title',)

    def message_user(self, *args, **kwargs):
        pass

    def save_model(self, request, obj, form, change):
        if change:
            if obj.status == '1':
                obj = form.save()
                obj.article.status = '3'
                obj.article.save()

                obj.status = '2'
                obj.save()

                for referee in obj.referees.all():
                    Review.objects.get_or_create(
                        assignment=obj, referee=referee)

                # * send email to referees
                from django.contrib.sites.shortcuts import get_current_site
                from django.core.mail import EmailMessage
                from django.urls import reverse
                for referee in obj.referees.all():
                    email = EmailMessage(
                        subject='Asignación de artículo',
                        body=f'Estimado(a) {referee.user.get_full_name()},\n\n'
                        f'Le informamos que ha sido asignado como árbitro del artículo {obj.article.title}.\n\n'
                        f'Para acceder al arbitraje del artículo puede verlo en su tablero de actividades, por favor ingrese a la siguiente dirección:\n\n'
                        f'{get_current_site(request).domain + reverse("core_dashboard:dashboard")}\n\n'
                        f'Atentamente,\n\n'
                        f'Comité Editorial de Ciencia y Tecnología',
                        from_email='jonathan90090@gmail.com',
                        to=[referee.user.email]
                    )

                    email.send()
                messages.success(
                    request,
                    format_html(
                        'La asignación del artículo <a>' + obj.article.title + '</a> se ha actualizado correctamente'))
                obj.save()
            else:
                messages.success(
                    request,
                    format_html(
                        'La asignación del artículo <a>' + obj.article.title + '</a> se ha actualizado correctamente'))
                
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        messages.success(request,
                         format_html(
                             'La asignación del artículo' + obj.article.title + ' se ha eliminado correctamente'))
        obj.delete()


class ArticleProfileAdmin(admin.ModelAdmin):

    readonly_fields = ('article', 'publication', 'status')

    def get_perfiles_article(self, obj):
        return format_html('<br>'.join(
            ['<a href="/admin/Asignacion_Arbitros/profile/' + str(p.id) + '/change/">' + str(p) + '</a>' for p in obj.profiles.all()]))

    get_perfiles_article.short_description = 'Perfiles'

    def assignment_link(self, obj):

        if obj.status == 'A':
            return format_html('<a href="/admin/Asignacion_Arbitros/assignment/' + str(obj.article.assignment.id) + '/change/">' + ('Asignar' if obj.article.status == '2' else 'Ver') + '</a>')

    assignment_link.short_description = 'Asignación'

    list_display = ('article', 'get_perfiles_article',
                    'status', 'assignment_link')

    list_filter = ('status', 'profiles')

    search_fields = ('article__title',
                     'profiles__user__first_name', 'profiles__user__last_name')

    def message_user(self, *args, **kwargs):
        pass

    # * create assigment for each article when update and status is 2
    def save_model(self, request, obj, form, change):
        if change:
            print(form.cleaned_data['profiles'].count())
            if 'profiles' in form.changed_data and (form.cleaned_data['profiles'].count() != 0 or len(form.initial['profiles']) != 0):

                Assignment.objects.get_or_create(
                    article=obj.article,
                    publication=obj.publication,
                )
                obj.status = 'A'
                obj.save()

            else:
                obj.status = 'P'
                obj.save()
            messages.success(request, format_html(
                'El artículo <a>' + obj.article.title + '</a> se ha actualizado correctamente'))
        else:

            messages.success(request, format_html(
                'El artículo <a>' + obj.article.title + '</a> se ha creado correctamente'))


admin.site.register(Assignment, AssignmentAdmin)

admin.site.register(ArticleProfile, ArticleProfileAdmin)


class ProfileAdmin(admin.ModelAdmin):

    pass


admin.site.register(Profile, ProfileAdmin)
# * expresión regular para dos nombres máximo

reg = r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]{1,50}$'
