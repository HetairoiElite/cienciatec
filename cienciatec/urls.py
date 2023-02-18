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
from notifications import urls as notifications_urls


urlpatterns = [
    # path("chat/", include("apps.chat.urls")),
    
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),

    
    path('', include('core.urls')),

    path('accounts/', include('apps.registration.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('eventos/', include('apps.events.urls')),


    path('tablero/', include('apps.core_dashboard.urls')),
    
    # * celery_progress
    # path('celery-progress/', include('celery_progress.urls')),
    
    # * proposal reception
    path('tablero/recepcion-propuestas/', include('apps.proposal_reception.urls')),

    re_path(r'^inbox/notifications/',
            include(notifications_urls, namespace='notifications')),
    
    
]

# * Custom titles for admin site
admin.site.site_header = "CienciaTec"
admin.site.index_title = "Panel de administración de CienciaTec"
admin.site.site_title = "CienciaTec"

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
