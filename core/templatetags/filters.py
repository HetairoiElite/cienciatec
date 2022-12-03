from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def to_and(value):
    print(value)
    print('1 minutos' in value)
    if '1 minutos' in value:
        value = value.replace('minutes', '1 minuto')
    else:
        value = value.replace("minutes", "minutos")
    lista = value.split(",")
    if len(lista) == 1:
        return value
    elif len(lista) > 1:
        return "".join(lista[:-1]) + ", " + lista[-1]


@register.filter
def minutes(value):
    # extract the minutes from the string
    minutes = value.split("\xa0")[0]

    return int(minutes)


@register.simple_tag
def live_notify_list_notis(list_class='live_notify_list'):
    # * bootstrap dropdown menu
    html = "<ul class='{list_class}'></ul>".format(list_class=list_class)
    # html = "<ul class='{list_class}'></ul>".format(list_class=list_class)
    return format_html(html)
