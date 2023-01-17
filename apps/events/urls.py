from django.urls import path

from . import views

# * app_name

app_name = 'events'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
]