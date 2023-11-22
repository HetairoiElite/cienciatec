from django.shortcuts import render
from apps.proposal_reception.models import ArticleProposal
from django.shortcuts import redirect
# Create your views here.

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.contrib import messages as message
from django.urls import reverse


class FinalReportAdminView(TemplateView):
    template_name = 'admin/final_report_admin.html'

    def get(self, request, *args, **kwargs):

        article = ArticleProposal.objects.get(id=kwargs['article_id'])
        action = kwargs['action']

        color = 'red' if action == 'rechazar' else 'green'
        context = {
            'article': article,
            'action': mark_safe(f'<span style="color: {color};">{action.capitalize()}</span>')
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        article = ArticleProposal.objects.get(id=kwargs['article_id'])
        action = kwargs['action']

        from dotenv import load_dotenv
        import os
        from django.conf import settings
        # Asegúrate de importar NamedTemporaryFile desde tempfile
        from tempfile import NamedTemporaryFile

        load_dotenv()

        DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

        if DJANGO_SETTINGS_MODULE == 'cienciatec.settings.prod':
            # Asegúrate de importar el modelo Home desde tu aplicación
            from core.models import Home
            from django.core.files.storage import default_storage

            home = Home.objects.first()

            if action == 'aceptar':
                template = home.report_letters.template_accepted.path
            else:
                template = home.report_letters.template_rejected.path


            # Crear archivos temporales para cada archivo
            temp_template = NamedTemporaryFile(delete=False)
            # Guardar cada archivo en su respectivo archivo temporal
            with default_storage.open(template) as f:
                with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename(template)), 'wb') as d:
                    d.write(f.read())
        else:
            # Asegúrate de importar el modelo Home desde tu aplicación
            from core.models import Home
            from django.core.files.storage import default_storage

            home = Home.objects.first()

            if action == 'aceptar':
                template = home.report_letters.template_accepted.path
            else:
                template = home.report_letters.template_rejected.path

            # Crear archivos temporales para cada archivo
            temp_template = NamedTemporaryFile(delete=False)
            # Guardar cada archivo en su respectivo archivo temporal
            with default_storage.open(template) as f:
                with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename(template)), 'wb') as d:
                    d.write(f.read())

        if action == 'aceptar':
            article.status = '8'
        else:
            article.status = '9'

        article.save()

        article.send_arbitration_report()

        if action == 'rechazar':
            message.success(
                request, mark_safe(f"""La propuesta de artículo <a href="{reverse("admin:Recepcion_Propuestas_articleproposal_change", args=[article.id])}">{article.title}</a> ha sido 
                                   <span style="color: red;">
                                   rechazada
                                      </span>
                                   exitosamente."""))
        else:
            # * agregar un mensaje de exito
            message.success(
                request, mark_safe(f"""La propuesta de artículo <a href="{reverse("admin:Recepcion_Propuestas_articleproposal_change", args=[article.id])}">{article.title}</a> ha sido
                                   <span style="color: green;">
                                   aceptada
                                        </span>
                                   exitosamente."""))

        return redirect('admin:Recepcion_Propuestas_articleproposal_changelist')
