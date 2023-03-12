from django.shortcuts import render
from django.views.generic import UpdateView
from .models import ArticleCorrection
from .forms import CorrectionReceptionForm
from apps.article_review.models import Note
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
# Create your views here.


class CorrectionFormView(UpdateView):
    model = ArticleCorrection
    template_name = 'correction_reception/correction_form.html'
    context_object_name = 'correction'

    form_class = CorrectionReceptionForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile != self.get_object().article.author:
            messages.error(
                request, 'No tienes permiso para acceder a esta página')
            return redirect('core_dashboard:dashboard')

        if self.get_object().correction_file:
            messages.error(request, 'Ya has enviado tu corrección')
            return redirect('core_dashboard:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        object = self.get_object()

        notes = Note.objects.filter(
            review__assignment__article=object.article)

        form = CorrectionReceptionForm(instance=object)

        return render(request, self.template_name, {
            'form': form, 'correction': self.get_object(), 'notes': notes
        })

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        form = CorrectionReceptionForm(
            request.POST, request.FILES, instance=object)
        notes = Note.objects.filter(
            review__assignment__article=object.article)
        if form.is_valid():
            form.save()
            return redirect('core_dashboard:dashboard')
        else:
            return render(request, self.template_name, {
                'form': form, 'correction': self.get_object(), 'notes': notes
            })
