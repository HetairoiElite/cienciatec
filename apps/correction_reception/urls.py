from django.urls import path

from .views import CorrectionFormView, DictamenView

app_name = 'correction_reception'

urlpatterns = [
    path('<int:pk>/', CorrectionFormView.as_view(), name='correction_form'),
    path('dictamen/<int:pk>/', DictamenView.as_view(), name='dictamen'),
    
]