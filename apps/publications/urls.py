from django.urls import path

from . import views

# * app_name

app_name = 'publications'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('articulo/<int:pk>/', views.ArticleView.as_view(), name='article_detail'),
    
]