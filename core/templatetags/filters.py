from django import template

register = template.Library()

@register.filter
def to_and(value):
    value = value.replace("minutes","minutos")
    lista = value.split(",")
    if len(lista) == 1:
        return value
    elif len(lista) > 1:
        return "".join(lista[:-1]) + ", " + lista[-1]

@register.filter
def minutes(value):
    # extract the minutes from the string
    minutes = value.split("\xa0")[0]
    
    print(minutes)
    return int(minutes)