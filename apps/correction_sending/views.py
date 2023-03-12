from django.views.generic import View
from .forms import CorrectionSendingForm
from apps.article_review.models import Review
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.
from apps.correction_reception.models import ArticleCorrection

# * Importar los modelos


class CorrectionSendingView(View):

    def post(self, request, *args, **kwargs):

        # * get review
        review = Review.objects.get(pk=kwargs['pk'])

        form = CorrectionSendingForm(request.POST)

        if form.is_valid():
            # * Hacer algo con el formulario
            val = form.cleaned_data.get('btn')

            if val == 'Si':

                review.enviado = True
                
                review.save()

                assignment = review.assignment

                # * if all reviews are sent then change the status of assignment to completed

                # * get all reviews of the assignment

                reviews = Review.objects.filter(assignment=assignment)

                # * check if all reviews are sent

                for review in reviews:
                    if review.enviado == False:
                        messages.success(
                            request, 'Se ha cargado la corrección. Se notificará al autor cuando se hayan cargado todas las correcciones pendientes por los otros arbitros.')
                        return redirect('core_dashboard:dashboard')
                else:
                    assignment.completed = True
                    assignment.save()
                    
                    ArticleCorrection.objects.get_or_create(article=assignment.article)
                    
                    
                    messages.success(
                        request, 'Se ha enviado la corrección y se ha notificado al autor.')

                    from django.contrib.sites.shortcuts import get_current_site
                    from django.core.mail import EmailMessage
                    from django.urls import reverse

                    email = EmailMessage(
                        subject='Artículo arbitrado',
                        body=f'Estimado(a) {review.assignment.article.author.user.get_full_name()},\n\n'
                        f'Le informamos que el artículo {review.assignment.article.title} ha sido arbitrado y tiene correciones pendientes por realizar.\n\n'
                        f'Para acceder al artículo puede verlo en su tablero de actividades, por favor ingrese a la siguiente dirección:\n\n'
                        f'{get_current_site(request).domain + reverse("core_dashboard:dashboard")}\n\n'
                        f'Atentamente,\n\n'
                        f'Comité Editorial de Ciencia y Tecnología',
                        from_email='jonathan90090@gmail.com',
                        to=[review.assignment.article.author.user.email]
                    )

                    email.send()

                    return redirect('core_dashboard:dashboard')

        else:
            return redirect('core_dashboard:dashboard')
