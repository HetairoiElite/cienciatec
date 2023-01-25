from django.shortcuts import render
from notifications.signals import notify
from django.contrib.auth.models import User

from django.views.generic import TemplateView

# * login required mixin
from django.contrib.auth.mixins import LoginRequiredMixin


# * apps
from apps.chat.models import Thread


# Create your views here.


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'core_dashboard/index.html'


# class ProposalArticleDetail(LoginRequiredMixin, TemplateView):
#     template_name = 'proposal_reception/article_proposal_detail.html'