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
            events_html += f'<li> Inicio {event.get_absolute_url()} </li>'

        for event in events_from_day_end:
            events_html += f'<li> Final {event.get_absolute_url()} </li>'

        if events:
            # * recepcion de propuestas
            rp = events[0].proposal_reception

            if rp.start_date.day == day and rp.start_date.month == self.month and rp.start_date.year == self.year:
                events_html += f'<li> Inicio {rp} </li>'
            elif rp.end_date.day == day and rp.end_date.month == self.month and rp.end_date.year == self.year:
                events_html += f'<li> Final {rp} </li>'

            # * asignacion de articulos
            aa = events[0].reviewer_assignment

            if aa.start_date.day == day and aa.start_date.month == self.month and aa.start_date.year == self.year:
                events_html += f'<li> Inicio {aa} </li>'
            elif aa.end_date.day == day and aa.end_date.month == self.month and aa.end_date.year == self.year:
                events_html += f'<li> Final {aa} </li>'

            # * revision de articulos
            ra = events[0].article_review

            if ra.start_date.day == day and ra.start_date.month == self.month and ra.start_date.year == self.year:
                events_html += f'<li> Inicio {ra} </li>'
            elif ra.end_date.day == day and ra.end_date.month == self.month and ra.end_date.year == self.year:
                events_html += f'<li> Final {ra} </li>'

            # * envio de correcciones
            cs = events[0].corrections_sending

            if cs.start_date.day == day and cs.start_date.month == self.month and cs.start_date.year == self.year:
                events_html += f'<li> Inicio {cs} </li>'
            elif cs.end_date.day == day and cs.end_date.month == self.month and cs.end_date.year == self.year:
                events_html += f'<li> Final {cs} </li>'

            # * recepcion de correcciones
            cr = events[0].corrections_reception

            if cr.start_date.day == day and cr.start_date.month == self.month and cr.start_date.year == self.year:
                events_html += f'<li> Inicio {cr} </li>'
            elif cr.end_date.day == day and cr.end_date.month == self.month and cr.end_date.year == self.year:
                events_html += f'<li> Final {cr} </li>'

            # * envio de dictamen final
            fs = events[0].final_report_sending

            try:

                if fs.day == date(self.year, self.month, day):
                    events_html += f'<li>{fs} </li>'

                # * publicacion de articulos
                pa = events[0].article_publication

                if pa.day == date(self.year, self.month, day):
                    events_html += f'<li>{pa} </li>'
            except:
                pass

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:

            if date.today() == date(self.year, self.month, day):
                # * si el dia está entre el rango de

                return '<td class="%s today">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
            else:
                if events.filter(Q(end_date__gte=date(self.year, self.month, day)) & Q(start_date__lte=date(self.year, self.month, day))):
                    return '<td class="%s event">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
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
