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
# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    list_display = ['numero_publicacion', 'start_date', 'end_date']
    change_list_template = 'admin/events/change_list.html'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['numero_publicacion', 'home', 'numero_folio']
        else:
            return ['home']

    def get_exclude(self, request, obj=None):
        if obj:
            return []
        else:
            return ['current']

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


admin.site.register(Publication, PublicationAdmin)