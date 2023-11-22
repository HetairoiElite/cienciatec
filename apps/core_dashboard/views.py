from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

# * login required mixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# * apps
# from apps.chat.models import Thread


from apps.events.models import Publication
# Create your views here.

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'core_dashboard/index.html'
    

    from django.utils import timezone

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        publicacion = Publication.objects.get_current()
        from django.utils import timezone
        now = timezone.now()

        # * si el usuario es un autor o un editor
        if request.user.profile.type_user == '1' or request.user.profile.type_user == '2':
            if not publicacion:
                # * mensaje
                messages.error(
                    request, 'No hay un periodo de publicación disponible.')
                return redirect('home')
            elif not (publicacion.start_date <= now <= publicacion.end_date):
                messages.error(
                    request, 'Actualmente no estamos dentro de un periodo de publicación o el periodo de publicación puede haber terminado. Por favor, regrese más tarde cuando un nuevo periodo de publicación esté activo.')
                return redirect('home')
        else:
            return redirect('home')
        
        # if request.user.profile.type_user == '2':
            

        return super().dispatch(request, *args, **kwargs)
# class ProposalArticleDetail(LoginRequiredMixin, TemplateView):
#     template_name = 'proposal_reception/article_proposal_detail.html'