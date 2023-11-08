from django.urls import path
from .views import ObservationSendingView

app_name = 'observation_sending'

urlpatterns = [
    path('observation_sending/<int:pk>/', ObservationSendingView.as_view(), name='observation_sending'),
]