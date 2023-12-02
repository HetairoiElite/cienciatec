from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import TemplateView
# Create your views here.
from . models import Publication, Article
from apps.proposal_reception.models import ArticleProposal

from django.urls import reverse
from django.utils.safestring import mark_safe
from .utils import PublicationCalendar
import calendar
import datetime

from django.contrib import messages as message


class CalendarView(ListView):
    model = Publication
    template_name = 'events/calendario.html'
    context_object_name = 'publications'

    def get_context_data(self, **kwargs):
        after_day = self.request.GET.get('start_date__gte', None)
        context = {}

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

        context['previous_month'] = reverse('events:calendar') + '?start_date__gte=' + str(
            previous_month)
        context['next_month'] = reverse(
            'events:calendar') + '?start_date__gte=' + str(next_month)

        cal = PublicationCalendar()

        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)

        # * traducir meses

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

        html_calendar = html_calendar.replace(
            '<td ', '<td  width="200" height="50"')

        html_calendar = html_calendar.replace(
            'class="calendar"', 'class="calendar table table-bordered border-primary"')

        context['calendar'] = mark_safe(html_calendar)

        # print(html_calendar)

        return context

class PublicationView(TemplateView):
    template_name = 'admin/publication_confirm.html'

    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        article = ArticleProposal.objects.get(id=kwargs['article_id'])
        context['article'] = article
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        from django.utils import timezone
        article_proposal = ArticleProposal.objects.get(id=kwargs['article_id'])
        
        article_proposal.status = '10'
        
        
        
        
        article = Article.objects.create(
            publication=article_proposal.publication,
            article_proposal=article_proposal,
            fecha_publicacion=timezone.now()
        )
        
        article.publicar()
        article_proposal.save()
        
        message.success(
                request, mark_safe(f"""La propuesta de artículo <a href="{reverse("admin:Eventos_article_change", args=[article.id])}">{article.article_proposal.title}</a> ha sido
                                   <span style="color: green;">
                                   Publicada
                                        </span>
                                   exitosamente."""))

        return redirect('admin:Recepcion_Propuestas_articleproposal_changelist')
    
class ArticleView(TemplateView):
    template_name = 'publications/article.html'
    
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(id=self.kwargs['pk'])
        context = {
            'article': article
        }
        return render(request, self.template_name, context)