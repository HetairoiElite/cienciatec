from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

# * login required mixin
from django.contrib.auth.mixins import LoginRequiredMixin


# * apps
# from apps.chat.models import Thread


from apps.events.models import Publication
# Create your views here.

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'core_dashboard/index.html'
    

    def dispatch(self, request, *args, **kwargs):
        publicacion = Publication.objects.get_current()
        
        if not publicacion:
            # * mensaje
            messages.error(
                request, 'No hay un periodo de publicación disponible.')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)
# class ProposalArticleDetail(LoginRequiredMixin, TemplateView):
#     template_name = 'proposal_reception/article_proposal_detail.html'