from django.urls import path
from .views import *

app_name = 'registration'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('sent_email/', SentEmailView, name='sent_email'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('test_email/', test_email, name='test_email'),
    path('activate/<uidb64>/<token>/', activeEmail, name='activate'),
    path('email/resend_link/',
         new_link_active_email, name='resend_link_email'),
    path('profile/', UpdateProfile.as_view(), name='profile'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
]
