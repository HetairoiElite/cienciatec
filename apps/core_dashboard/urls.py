from django.urls import path

from .views import *

app_name = 'core_dashboard'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
]
 
