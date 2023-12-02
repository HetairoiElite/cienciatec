"""cienciatec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings

from jet.dashboard.dashboard_modules import google_analytics_views
from django.utils.translation import gettext_lazy as _
from jet.dashboard.dashboard import DefaultIndexDashboard
from jet.dashboard.dashboard_modules import google_analytics
from apps.proposal_reception.dashboard_modules import RecentArticleProposals
from apps.registration.dashboard_modules import NewUsers

class CustomIndexDashboard(DefaultIndexDashboard):
    columns = 3

    def init_with_context(self, context):
        super(CustomIndexDashboard, self).init_with_context(context)
        self.available_children.append(RecentArticleProposals)
        self.children.append(RecentArticleProposals)
        self.available_children.append(NewUsers)
        self.children.append(NewUsers)

from apps.final_report_sending.views import FinalReportAdminView

urlpatterns = [
    # path("chat/", include("apps.chat.urls")),

    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    
    # path('admin/dictamen-final/', include('apps.final_report_sending.urls',
    #      namespace='final_report_sending')),

    path('admin/dictamen-final/', include('apps.final_report_sending.urls')),
    path('admin/', admin.site.urls),



    path('', include('core.urls')),

    path('accounts/', include('apps.registration.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('publicacion/', include('apps.publications.urls')),


    path('tablero/', include('apps.core_dashboard.urls')),

    # * celery_progress
    # path('celery-progress/', include('celery_progress.urls')),

    # * proposal reception
    path('tablero/recepcion-propuestas/',
         include('apps.proposal_reception.urls')),


    # * article review
    path('tablero/revision-articulos/', include('apps.article_review.urls')),


    # * correction sending
    path('tablero/envio-correcciones/', include('apps.observation_sending.urls')),

    # * correction reception
    path('tablero/recepcion-correcciones/',
         include('apps.correction_reception.urls')),
]

# * Custom titles for admin site
admin.site.site_header = "100CIATEC"
admin.site.index_title = "Panel de administración de CienciaTec"
admin.site.site_title = "100CIATEC"


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
