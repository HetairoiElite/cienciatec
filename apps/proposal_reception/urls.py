from django.urls import path

from . import views

app_name = 'proposal_reception'

urlpatterns = [
    path('', views.ProposalFormView.as_view() , name='article_proposal_form'),
]