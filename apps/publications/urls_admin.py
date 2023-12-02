from django.urls import path
from .views import PublicationView
from django.contrib import admin

app_name = 'admin_publications'

urlpatterns = [
    path('<int:article_id>/',
         admin.site.admin_view(PublicationView.as_view()), name='publication_article_admin'),

]
