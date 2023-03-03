from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
# Register your models here.

from .models import *
from .forms import AssignmentForm
from apps.article_review.models import Review


class AssignmentAdmin(admin.ModelAdmin):

    form = AssignmentForm

    def get_referees(self, obj):
        return format_html('\n'.join(

            ['<a href="/admin/auth/user/' + str(p.id) + '/change/#/tab/inline_0/">' +
             p.user.get_full_name() + '</a>' for p in obj.referees.all()]))
    get_referees.short_description = 'Árbitros'

    def get_profiles(self, obj):
        return format_html('<br>'.join(
            ['<a href="/admin/Asignacion_Arbitros/profile/' + str(p.id) + '/change/">' + str(p) + '</a>' for p in obj.article.profile.profiles.all()]))

    get_profiles.short_description = 'Perfiles'

    list_display = ('article', 'get_referees', 'status')

    readonly_fields = ('article', 'publication', 'get_profiles')

    def message_user(self, *args, **kwargs):
        pass

    def save_model(self, request, obj, form, change):
        if change:

            if 'referees' in form.changed_data and form.cleaned_data['referees'].count() > 0 or obj.referees.count() > 0:
                obj = form.save()
                obj.status = 'A'

                for referee in obj.referees.all():
                    Review.objects.get_or_create(assignment=obj, referee=referee)
                
                
                
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

            else:
                obj.status = 'P'
                Review.objects.filter(assignment=obj).delete()
            messages.success(
                request,
                format_html(
                    'La asignación del artículo <a>' + obj.article.title + '</a> se ha actualizado correctamente'))

            if 'referees' in form.changed_data and form.cleaned_data['referees'].count() == 0:
                obj.status = 'P'
                messages.warning(
                    request,
                    format_html(
                        'La asignación del artículo <a>' + obj.article.title + '</a> no tiene árbitros asignados'))
        else:
            messages.success(request,
                             format_html(
                                 'La asignación del artículo <a>' + obj.article.title + '</a> se ha creado correctamente'))

        obj.save()

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

    list_display = ('article', 'get_perfiles_article', 'status')

    list_filter = ('status', 'profiles')

    search_fields = ('article__title',
                     'profiles__user__first_name', 'profiles__user__last_name')

    def message_user(self, *args, **kwargs):
        pass

    # * create assigment for each article when update and status is 2
    def save_model(self, request, obj, form, change):
        if change:
            if 'profiles' in form.changed_data and form.cleaned_data['profiles'].count() > 0 or obj.profiles.count() > 0:

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
admin.site.register(Profile)
# * expresión regular para dos nombres máximo

reg = r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]{1,50}$'
