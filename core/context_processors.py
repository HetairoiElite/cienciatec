# * context procesor for home

from .models import Home
from apps.events.models import Publication


def home(request):
    home = Home.objects.first()
    current_publication = Publication.objects.get_current()
    context = {
        'home': home,
        'current_publication': current_publication,
    }
    return context
