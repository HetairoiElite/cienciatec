from django.shortcuts import render
from notifications.signals import notify
from django.contrib.auth.models import User
from apps.chat.models import Thread
# Create your views here.


def dashboard(request):
    
    return render(request, 'dashboard/index.html')
