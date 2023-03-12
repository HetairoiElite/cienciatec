from django.urls import path

from .views import CorrectionFormView

app_name = 'correction_reception'

urlpatterns = [
    path('<int:pk>/', CorrectionFormView.as_view(), name='correction_form'),
]