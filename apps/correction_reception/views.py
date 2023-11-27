from django.views.generic import View
from apps.article_review.models import Review
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
                request, 'No tienes permiso para acceder a esa página.')
            return redirect('core_dashboard:dashboard')

        if self.get_object().article.status != '4':
            messages.error(request, 'Ya has enviado tus correcciones.')
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
            article_correction = form.save()
            article_correction.generate_correction_file_as_pdf()
            article_correction.article.status = '5'
            article_correction.article.save()
            article_correction.article.assignment.status = '5'
            article_correction.article.assignment.save()

            # * enviar correo a los arbitros

            from django.core.mail import send_mail
            from django.conf import settings
            from django.contrib.sites.shortcuts import get_current_site
            from django.urls import reverse

            subject = 'Recepción de correcciónes'

            message = f"""
            El autor ha cargado la corrección del artículo. Por favor, revisa la corrección y envía tu decisión.
            
            Accede a la plataforma para revisar las correcciones en el siguiente enlace:
            
            { get_current_site(request).domain + reverse('core_dashboard:dashboard')}
            
            
            """

            from_email = settings.EMAIL_HOST_USER

            to_list = [
                review.referee.user.email for review in article_correction.article.assignment.reviews.all()]

            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(
                request, 'Se ha enviado la corrección para su dictamen final')

            return redirect('core_dashboard:dashboard')
        else:
            return render(request, self.template_name, {
                'form': form, 'correction': self.get_object(), 'notes': notes
            })


class DictamenView(View):

    def dispatch(self, request, *args, **kwargs):
        review = Review.objects.get(pk=kwargs['pk'])

        if review.referee != request.user.profile:
            messages.error(
                request, 'No tienes permiso para acceder a esa página.')
            return redirect('core_dashboard:dashboard')

        if review.dictamen != None:
            messages.error(request, 'Ya has realizado tu dictamen')

            return redirect('core_dashboard:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        review = Review.objects.get(pk=kwargs['pk'])
        
        from .forms import ReportForm
        
        form = ReportForm(request.POST)
        
        if form.is_valid():
            dictamen = form.cleaned_data['dictamen']
            
            if dictamen == 'Aceptar':
                review.dictamen = '1'
            else:
                review.dictamen = '2'
                
            review.save()
            review.assignment.status = '6'
            review.assignment.save()
            review.assignment.article.status = '6'
            review.assignment.article.save()
            
            reported_reviews = Review.objects.get_reported_reviews(review.assignment)
            
            if reported_reviews == 2:
                review.assignment.status = '7'
                review.assignment.article.status = '7'
                review.assignment.article.save()
                review.assignment.completed = True
                review.assignment.save()

                
                
            
            messages.success(request, 'Dictamen guardado. Gracias por tu colaboración')
            
            return redirect('core_dashboard:dashboard')
        else:
            return redirect('core_dashboard:dashboard')