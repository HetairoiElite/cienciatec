
# * imports


# * django
from django.utils import timezone

from django.shortcuts import render
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

from django.views.generic import TemplateView, UpdateView

# * locals

from .forms import ArticleProposalForm, CoauthorForm, ArticleImageForm, ArticleProposalUpdateForm
from .models import ArticleProposal, Coauthor, ArticleImage

# * home
from apps.events.models import Publication

# *¨login required mixin
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# * article proposal form view
publication = Publication.objects.get_current()


class ProposalFormView(LoginRequiredMixin, TemplateView):
    template_name = 'proposal_reception/article_proposal_form.html'

    def get(self, request, *args, **kwargs):
        article_proposal_form = ArticleProposalForm()

        # * coauthor formset

        CoauthorFormSet = inlineformset_factory(
            ArticleProposal,
            Coauthor,
            form=CoauthorForm,
            extra=0,
            can_delete=False
        )

        coauthor_formset = CoauthorFormSet()

        # * article image formset

        ArticleImageFormSet = inlineformset_factory(
            ArticleProposal,
            ArticleImage,
            form=ArticleImageForm,
            extra=0,
            can_delete=False
        )

        article_image_formset = ArticleImageFormSet()

        context = {

            'article_proposal_form': article_proposal_form,
            'coauthor_formset': coauthor_formset,
            'article_image_formset': article_image_formset,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        article_proposal_form = ArticleProposalForm(
            request.POST, request.FILES)

        # * coauthor formset

        CoauthorFormSet = inlineformset_factory(
            ArticleProposal,
            Coauthor,
            form=CoauthorForm,
            extra=0,
            can_delete=False
        )

        coauthor_formset = CoauthorFormSet(request.POST)

        # * article image formset

        ArticleImageFormSet = inlineformset_factory(
            ArticleProposal,
            ArticleImage,
            form=ArticleImageForm,
            extra=0,
            can_delete=False
        )

        article_image_formset = ArticleImageFormSet(
            request.POST, request.FILES)

        if article_proposal_form.is_valid() and coauthor_formset.is_valid() and article_image_formset.is_valid():
            article_proposal = article_proposal_form.save(commit=False)
            article_proposal.author = request.user.profile

            article_proposal.proposal_reception = publication.proposal_reception

            article_proposal.save()

            coauthor_formset.instance = article_proposal
            coauthor_formset.save()

            article_image_formset.instance = article_proposal
            article_image_formset.save()

            messages.success(request, 'Propuesta enviada con éxito')
            
            return redirect('core_dashboard:dashboard')

        context = {

            'article_proposal_form': article_proposal_form,
            'coauthor_formset': coauthor_formset,
            'article_image_formset': article_image_formset,
        }

        return render(request, self.template_name, context)

    # * if artiproposal date is over, add error message

    def dispatch(self, request, *args, **kwargs):

        # * fecha actual
        now = timezone.now()

        print(now)

        if now > publication.proposal_reception.end_date:
            # ¨* add error message

            messages.error(
                request, 'El periodo de recepción de propuestas ha finalizado')

            return redirect(reverse('index') + '#over')

        return super().dispatch(request, *args, **kwargs)

class ArticleProposalUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'proposal_reception/article_proposal_update.html'

    model = ArticleProposal
    
    context_object_name = 'article_proposal'
        
    form_class = ArticleProposalUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        # * login required
        
        # * if artiproposal date is over, add error message
        
        # * fecha actual
        now = timezone.now()
        
        print(now)
        
        if now > publication.proposal_reception.end_date:
            # ¨* add error message
            
            messages.error(
                request, 'El periodo de recepción de propuestas ha finalizado')
            
            return redirect(reverse('core_dashboard:dashboard') + '#over')
        
        # * if no session 
        if self.request.user.is_authenticated:
        
            if self.get_object().author != self.request.user.profile:
                messages.error(request, 'No tienes permisos para editar esa propuesta')
                return redirect('core_dashboard:dashboard')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, 'Propuesta actualizada con éxito')
        return reverse('core_dashboard:dashboard')
    
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        form = self.get_form()
        
        coauthor_formset = inlineformset_factory(
            ArticleProposal,
            Coauthor,
            form=CoauthorForm,
            extra=0,
            can_delete=True
        )(instance=self.object)
        
        article_image_formset = inlineformset_factory(
            ArticleProposal,
            ArticleImage,
            form=ArticleImageForm,
            extra=0,
            can_delete=True
        )(instance=self.object)
        
        context = self.get_context_data(
            form=form,
            coauthor_formset=coauthor_formset,
            article_image_formset=article_image_formset
        )
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
       
        self.object = self.get_object()
        
        form = self.get_form()
        
        coauthor_formset = inlineformset_factory(
            ArticleProposal,
            Coauthor,
            form=CoauthorForm,
            extra=0,
            can_delete=True
        )(request.POST, instance=self.object)
         
        article_image_formset = inlineformset_factory(
            ArticleProposal,
            ArticleImage,
            form=ArticleImageForm,
            extra=0,
            can_delete=True
        )(request.POST, request.FILES, instance=self.object)
        
        
        if form.is_valid() and article_image_formset.is_valid() and coauthor_formset.is_valid():
            return self.form_valid(form, coauthor_formset, article_image_formset)
        else:
            return self.form_invalid(form, coauthor_formset, article_image_formset)
         
        # if form.is_valid() and coauthor_formset.is_valid() and article_image_formset.is_valid():
        #     return self.form_valid(form, coauthor_formset, article_image_formset)
        # else:
        #     return self.form_invalid(form, coauthor_formset, article_image_formset)
        
    def form_valid(self, form, coauthor_formset, article_image_formset):
        self.object = form.save()
        coauthor_formset.save()
        article_image_formset.save()
        return super().form_valid(form)
    
    def form_invalid(self, form, coauthor_formset, article_image_formset):
        return self.render_to_response(self.get_context_data(form=form, coauthor_formset=coauthor_formset, article_image_formset=article_image_formset))
    
# from .tasks import go_to_sleep

# def prueba(request):
#     go_to_sleep.delay(5)
#     return render(request, 'proposal_reception/prueba.html')