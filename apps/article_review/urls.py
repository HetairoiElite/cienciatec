from django.urls import path
from . import views

app_name = 'article_review'


urlpatterns = [
    path('<int:pk>/', views.ReviewUpdateView.as_view(), name='review_detail'),
]