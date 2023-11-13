# * Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from apps.events.models import Publication

class OnlyAuthorMixin(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        
        if response.status_code == 302:
            return response
        
        
        publicacion = Publication.objects.get_current()
        
        # * si el usuario es un autor o un editor
        if request.user.profile.type_user == '1' or request.user.profile.type_user == '2':
            if not publicacion:
                # * mensaje
                messages.error(
                    request, 'No hay un periodo de publicación disponible.')
                return redirect('home')
            else:
                if request.user.profile.type_user == '2':
                    return redirect('core_dashboard:dashboard')
        else:
            return redirect('home')
        
        return super().dispatch(request, *args, **kwargs)