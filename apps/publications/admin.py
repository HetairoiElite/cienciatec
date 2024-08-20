from django.contrib import admin
from .models import *
import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from .utils import PublicationCalendar
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.utils.html import format_html
from .models import Article
# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    list_display = ['numero_publicacion', 'start_date', 'end_date']
    change_list_template = 'admin/publications/change_list.html'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['numero_publicacion', 'home', 'numero_folio']
        else:
            return ['home']

    def get_exclude(self, request, obj=None):
        if obj:
            return []
        else:
            return ['current', 'numero_folio']
        
    

    inlines = [
       
    ]


    # radio_fields = {
    #     'home': admin.VERTICAL,
    # }

    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('start_date__gte', None)
        extra_context = extra_context or {}

        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(
                    split_after_day[1]), day=1)
            except:
                d = datetime.date.today()

        # find first day of current month
        previous_month = datetime.date(year=d.year, month=d.month, day=1)
        previous_month = previous_month - \
            datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month

        last_day = calendar.monthrange(d.year, d.month)
        # find last day of current month
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])
        next_month = next_month + \
            datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month

        try:
            extra_context['previous_month'] = reverse('admin:Eventos_publication_changelist') + '?start_date__gte=' + str(
                previous_month)
            extra_context['next_month'] = reverse(
                'admin:Eventos_publication_changelist') + '?start_date__gte=' + str(next_month)

            cal = PublicationCalendar()
            html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
            html_calendar = html_calendar.replace(
                '<td ', '<td  width="200" height="150"')
            html_calendar = html_calendar.replace(
                'January', 'Enero'
            ).replace(
                'February', 'Febrero'
            ).replace(
                'March', 'Marzo'
            ).replace(
                'April', 'Abril'
            ).replace(
                'May', 'Mayo'
            ).replace(
                'June', 'Junio'
            ).replace(
                'July', 'Julio'
            ).replace(
                'August', 'Agosto'
            ).replace(
                'September', 'Septiembre'
            ).replace(
                'October', 'Octubre'
            ).replace(
                'November', 'Noviembre'
            ).replace(
                'December', 'Diciembre'
            )

            # * traducir dias de la semana

            html_calendar = html_calendar.replace(
                'Mon', 'Lun'
            ).replace(
                'Tue', 'Mar'
            ).replace(
                'Wed', 'Mie'
            ).replace(
                'Thu', 'Jue'
            ).replace(
                'Fri', 'Vie'
            ).replace(
                'Sat', 'Sab'
            ).replace(
                'Sun', 'Dom'
            )
            extra_context['calendar'] = mark_safe(html_calendar)
            return super(PublicationAdmin, self).changelist_view(request, extra_context)
        except:
            return super(PublicationAdmin, self).changelist_view(request, extra_context)

    def message_user(self, *args, **kwargs):
        pass

    def save_model(self, request, obj, form, change):
        if change:
            messages.add_message(request, messages.SUCCESS,
                                 format_html('La <a href="{}">{}</a> ha sido actualizada correctamente.', reverse('admin:Eventos_publication_change', args=[obj.id]), obj))
        else:
            messages.add_message(request, messages.SUCCESS,
                                 format_html('La <a href="{}">{}</a> ha sido creada correctamente.', reverse('admin:Eventos_publication_change', args=[obj.id]), obj))

        super().save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):
        messages.add_message(request, messages.SUCCESS,
                             format_html('La <a href="{}">{}</a> ha sido eliminada correctamente.', reverse('admin:Eventos_publication_change', args=[obj.id]), obj))
        super().delete_model(request, obj)

class ArticleAdmin(admin.ModelAdmin):
    
    def get_title(self, obj):
        return obj.article_proposal.title
    
    def has_add_permission(self, request):
        return False
    
    actions = None
     
    get_title.short_description = 'Titulo'
    list_display = [ 'get_title','fecha_publicacion', 'doi']
    search_fields = ['article_proposal__title']
    list_filter = ['publication__numero_publicacion']
    list_per_page = 10
    
    
    def get_readonly_fields(self, request, obj=None):

        return ['publication', 'article_proposal', 'fecha_publicacion', 'file']

    # * cuando se actualiza el doi se debe enviar un correo al autor del articulo
    def save_model(self, request, obj, form, change):
        if 'doi' in form.changed_data:
            if obj.doi:
                from django.core.mail import EmailMessage
                from django.conf import settings
                from django.contrib.sites.shortcuts import get_current_site
                
                author = obj.article_proposal.author
                
                subject = 'DOI de su articulo'
                
                message = f'''
Estimado/a {author.user.first_name} {author.user.last_name}:

Le informamos que el DOI de su articulo {obj.article_proposal.title} ha sido actualizado a {obj.doi}.
'''

                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [author.user.email],
                    reply_to=[settings.EMAIL_HOST_USER],
                )
                
                email.send()
                obj.article_proposal.status = '11'
                obj.article_proposal.save()
            
        super().save_model(request, obj, form, change)
         
            
    


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Article,ArticleAdmin)
