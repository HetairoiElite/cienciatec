# chat/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    # path("", views.index, name="index"),
    path('', ThreadListView.as_view(), name='list_threads'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='detail_thread'),
    path('thread/<int:pk>/add_message/', add_message, name='add_message'),
    path('thread/start/<str:username>/', start_thread, name='start_thread'),
]
