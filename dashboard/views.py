from django.shortcuts import render
from notifications.signals import notify
from django.contrib.auth.models import User
from chat.models import Thread
# Create your views here.


def dashboard(request):
    sender = Thread.objects.get(id=1)
    recipient = User.objects.get(id=2)
    message = "This is an simple message"
    notify.send(sender, recipient=recipient, verb='Message',
                description=message)
    context = {
        'user': request.user
    }

    return render(request, 'dashboard/index.html', context)
