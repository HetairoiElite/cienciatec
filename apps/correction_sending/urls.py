from django.urls import path
from .views import CorrectionSendingView

app_name = 'correction_sending'

urlpatterns = [
    path('correction_sending/<int:pk>/', CorrectionSendingView.as_view(), name='correction_sending'),
]