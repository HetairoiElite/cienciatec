from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
# Register your models here.

from .models import *
from .forms import AssignmentForm


class AssignmentAdmin(admin.ModelAdmin):

    form = AssignmentForm

    def get_referees(self, obj):
        return format_html('\n'.join(

            ['<a href="/admin/auth/user/' + str(p.id) + '/change/#/tab/inline_0/">' +
             p.user.get_full_name() + '</a>' for p in obj.referees.all()]))
    get_referees.short_description = 'Árbitros'

    list_display = ('article', 'get_referees', 'status')

    readonly_fields = ('article', 'publication')

    def message_user(self, *args, **kwargs):
        pass

    def save_model(self, request, obj, form, change):
        if change:
            messages.success(
                request,
                format_html(
                    'La asignación del artículo <a>' + obj.article.title + '</a> se ha actualizado correctamente'))
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
    
    readonly_fields = ('article', 'publication')
    
    

admin.site.register(Assignment, AssignmentAdmin)

admin.site.register(ArticleProfile, ArticleProfileAdmin)
admin.site.register(Profile)
# * expresión regular para dos nombres máximo

reg = r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]{1,50}$'