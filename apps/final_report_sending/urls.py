from django.urls import path
from .views import FinalReportAdminView
from django.contrib import admin
app_name = 'final_report_sending'

urlpatterns = [
    path('<int:article_id>/<str:action>/',
         admin.site.admin_view(FinalReportAdminView.as_view()), name='final_report_admin'),

]
