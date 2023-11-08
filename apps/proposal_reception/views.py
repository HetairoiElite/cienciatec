
# * imports


# * django
from django.utils import timezone

from django.shortcuts import render
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

# * method decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView, UpdateView
from django.views.generic import View
from django.http.response import JsonResponse


# * locals

from .forms import ArticleProposalForm, CoauthorForm, ArticleImageForm, ArticleProposalUpdateForm
from .models import ArticleProposal, Coauthor, ArticleImage

# * home
from apps.events.models import Publication

# *¨login required mixin
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# * article proposal form view


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

        publication = Publication.objects.get_current()

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

            article_proposal.publication = publication

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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        publication = Publication.objects.get_current()

        if not publication:
            messages.error(
                request, 'No se ha definido un periodo de publicación')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)


class ArticleProposalUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'proposal_reception/article_proposal_update.html'

    model = ArticleProposal

    context_object_name = 'article_proposal'

    form_class = ArticleProposalUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # * login required
        publication = Publication.objects.get_current()

        # * if not publication

        if not publication:
            messages.error(
                request, 'No se ha definido un periodo de publicación.')
            return redirect('core_dashboard:dashboard')

        if request.user.profile != self.get_object().author:
            messages.error(
                request, 'No tienes permiso para editar esa propuesta.')
            return redirect('core_dashboard:dashboard')

        if self.get_object().status == '2':
            messages.error(
                request, 'No puedes editar esta propuesta porque ya fue recibida')
            return redirect('core_dashboard:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Propuesta actualizada con éxito.')
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

# * check title view (ajax)


class CheckTitleView(View):

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title', None)

        title = title.strip()

        print('hola')
        id = request.GET.get('id', None)
        try:
            data = {
                'is_taken': ArticleProposal.objects.filter(title__iexact=title).exclude(id=id).exists()
            }
        except:
            data = {
                'is_taken': ArticleProposal.objects.filter(title__iexact=title).exists()
            }
        return JsonResponse(data)
