from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from .models import Thread
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

@method_decorator(login_required, name='dispatch')
class ThreadListView(TemplateView):
    model = Thread

    template_name: str = 'chat/thread_list.html'

@method_decorator(login_required, name='dispatch')
class ThreadDetailView(DetailView):
    model = Thread

    def get_object(self):
        obj = super(ThreadDetailView, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404()
        return obj
    
    def get_context_data(self, **kwargs):
        obj = super(ThreadDetailView, self).get_object()
        context = super().get_context_data(**kwargs)
        context['room_name'] = obj.id
        return context


def add_message(request, pk):

    jsonresponse = {'created': False}
    if request.user.is_authenticated:
        contenido = request.GET.get('content', None)
        if contenido:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(
                user=request.user, content=contenido)
            thread.messages.add(message)
            jsonresponse['created'] = True
            jsonresponse['message'] = message.content
            jsonresponse['created_at'] = message.created.strftime("%d %B, %Y")
            if len(thread.messages.all()) is 1:
                jsonresponse['first'] = True
    else:
        raise Http404("Usuario no autenticado")
    return JsonResponse(jsonresponse)


@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('detail_thread', args=[thread.pk]))
