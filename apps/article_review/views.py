from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .forms import *
from .models import *
from django.urls import reverse

# Create your views here.


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'article_review/review_detail.html'
    context_object_name = 'review'

    form_class = ReviewForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()

        if review.referee != request.user.profile:
            messages.error(
                request, 'No tiene permisos para acceder a este recurso.')
            return redirect('core_dashboard:dashboard')

        if request.GET['recepcion'] != 'true':
           
            if review.enviado:
                messages.error(
                    request, 'El arbitraje ya fue enviado. No se puede modificar.')
                return redirect('core_dashboard:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('article_review:review_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(review=self.object)
        return context

    def get(self, request, *args, **kwargs):

        if request.GET['recepcion'] != 'true':

            form = ReviewForm(instance=self.get_object())
            
            print(form.save(commit=False).assignment)

            inline_notes_form = inlineformset_factory(
                Review,
                Note,
                form=NotesForm,
                extra=0,
                can_delete=True,
            )
            return render(request, self.template_name, {
                'form': form, 'review': self.get_object(),
                'inline_notes_form': inline_notes_form(instance=self.get_object()),
            })
        else:

            inline_notes_form = inlineformset_factory(
                Review,
                Note,
                form=NotesReceptionForm,
                extra=0,
                can_delete=False,
            )

            return render(request, self.template_name, {
                'review': self.get_object(),
                'inline_notes_form': inline_notes_form(instance=self.get_object()),
            })

    def post(self, request, *args, **kwargs):

        if request.GET['recepcion'] != 'true':

            form = ReviewForm(request.POST)

            inline_notes_form = inlineformset_factory(
                Review,
                Note,
                form=NotesForm,
                extra=0,
                can_delete=True,
            )(request.POST, instance=self.get_object())

            if form.is_valid() and inline_notes_form.is_valid():
                return self.form_valid(inline_notes_form)
            else:
                return self.form_invalid(inline_notes_form)
        else:
            inline_notes_form = inlineformset_factory(
                Review,
                Note,
                form=NotesReceptionForm,
                extra=0,
                can_delete=False,
            )(request.POST, instance=self.get_object())

            if inline_notes_form.is_valid():
                return self.form_valid(inline_notes_form)
            else:
                return self.form_invalid(inline_notes_form)

    def form_valid(self, form, inline_notes_form):
        self.object = form.save()
        inline_notes_form.save()
        messages.success(self.request, '¡Arbitraje guardado exitosamente!')
        return redirect('core_dashboard:dashboard')

    def form_valid(self, inline_notes_form):
        inline_notes_form.save()
        messages.success(self.request, '¡Arbitraje guardado exitosamente!')
        return redirect('core_dashboard:dashboard')

    def form_invalid(self, inline_notes_form):
        return render(self.request, self.template_name, {
            'review': self.get_object(),
            'inline_notes_form': inline_notes_form,
        })

    def form_invalid(self, form, inline_notes_form):
        return render(self.request, self.template_name, {
            'form': form, 'review': self.get_object(),
            'inline_notes_form': inline_notes_form,
        })
