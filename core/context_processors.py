# * context procesor for home

from .models import Home

def home(request):
    home = Home.objects.first()
    return {'home': home}

