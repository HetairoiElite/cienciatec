from django.urls import path

from . import views

app_name = 'proposal_reception'

urlpatterns = [
    path('crear/', views.ProposalFormView.as_view() , name='article_proposal_form'),
    path('<int:pk>/edit/', views.ArticleProposalUpdateView.as_view(), name='article_proposal_update'),
    path('check-title/', views.CheckTitleView.as_view(), name='check_title'),
    
    # path('prueba/', views.prueba, name='prueba')
]