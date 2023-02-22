from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from time import strftime
from .models import Event, Publication
from django.db.models import Q


class PublicationCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(PublicationCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(
            start_date__day=day, start_date__month=self.month, start_date__year=self.year)
        events_from_day_end = events.filter(
            end_date__day=day, end_date__month=self.month, end_date__year=self.year)

        events_html = ''

        for event in events_from_day:
            events_html += f'<li class="event"> Inicio {event.get_absolute_url()} </li>'

        for event in events_from_day_end:
            events_html += f'<li class="event"> Final {event.get_absolute_url()} </li>'

        
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            if date.today() == date(self.year, self.month, day):
                # * si el dia está entre el rango de

                return '<td class="%s today"><span class="badge">%d</span>%s</td>' % (self.cssclasses[weekday], day, events_html)
            else:
                if events.filter(Q(end_date__gte=date(self.year, self.month, day)) & Q(start_date__lte=date(self.year, self.month, day ))):
                    return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
                else:
                    return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year = theyear
        self.month = themonth

        events = Publication.objects.filter(
            Q(end_date__month=themonth) | Q(start_date__month=themonth) | Q(start_date__month=themonth-1) | Q(end_date__month=themonth+1))

        # * si el mes es mayor a febrero restar 1 al mes

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="calendar">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
