from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory


from .forms import *
from .models import *

# Create your views here.


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'article_review/review_detail.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(review=self.object)
        return context

    def get(self, request, *args, **kwargs):

        form = ReviewForm()

        inline_notes_form = inlineformset_factory(
            Review,
            Note,
            form=NotesForm,
            extra=5,
            can_delete=False,
        )

        return render(request, self.template_name, {
            'form': form, 'review': self.get_object(),
            'inline_notes_form': inline_notes_form(instance=self.get_object()),
        })
