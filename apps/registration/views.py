from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import *
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth.views import LoginView
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.


def SignUpView(request):
    form = UserCreationFromEmail(request.POST or None)
    form_profile = UserCreationFormType(request.POST or None)

    if request.method == 'POST' and form.is_valid() and form_profile.is_valid():
        user = form.save()
        profile = Profile.objects.get(user=user)
        profile.type_user = form_profile.cleaned_data['type_user']
        profile.save()

        # * send confirmation email

        if activateEmailSendLink(request, user, user.email):

            context = {
                'status': 'success',
            }

            return redirect(reverse('sent_email')+f"?status={context['status']}")

    return render(request, 'registration/signup.html', {'form': form, 'form_profile': form_profile})


def SentEmailView(request):
    if not request.GET.get('status'):
        return redirect('home')
    return render(request, 'registration/sent_email.html', {'status': request.GET.get('status')})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True


def test_email(request):
    subject = 'Confirmación de registro'
    html_messsage = render_to_string(
        'registration/email_verification_msg.html', {'user': "kuan"})
    plaint_message = strip_tags(html_messsage)
    email_from = 'jonathan90090@gmail.com'
    recipient_list = ['jonathan90090@gmail.com']

    mail.send_mail(subject, plaint_message, email_from,
                   recipient_list, html_message=html_messsage)
    return redirect('login')


def activateEmailSendLink(request, user, to_email):
    mail_subject = 'Activación de cuenta.'
    message = render_to_string(
        'registration/email_verification_msg.html', {
            'user': user.first_name + " " + user.last_name,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        })
    plaint_message = strip_tags(message)

    if send_mail(mail_subject, plaint_message, settings.EMAIL_HOST_USER, [to_email], html_message=message):
        return True
    else:
        return False


def reset_email_send_link(request, user, to_email):
    mail_subject = 'Cambio de contraseña.'
    message = render_to_string(
        'reset_password_mail.html', {
            'user': user.NombreCompleto(),
            'domain': "recover.applantar.com",
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https',
        })

    if send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email]):
        return True
    else:
        return False


def activeEmail(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not user.is_active and account_activation_token.check_if_token_expired(token):
            return render(request, 'registration/activate_email.html', {'status': 'warning', 'uidb64': uidb64, 'token': token})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activate_email.html', {'status': 'success'})
    else:
        return render(request, 'registration/activate_email.html', {'status': 'error'})


def new_link_active_email(request):
    try:
        uid = force_str(urlsafe_base64_decode(request.GET.get('uidb64')))
        user = User.objects.get(pk=uid)
        if not user.is_active:
            if activateEmailSendLink(request, user, user.email):
                context = {
                    'status': 'success',
                }
                return redirect(reverse('sent_email')+f"?status={context['status']}")
            else:
                context = {
                    'status': 'error',
                }
                return redirect(reverse('sent_email')+f'?status={context["status"]}')
        else:
            context = {
                'status': 'warning',
            }
            return redirect(reverse('sent_email')+f'?status={context["status"]}')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    context = {
        'status': 'error',
    }
    return redirect(reverse('sent_email')+f'?status={context["status"]}')


@login_required(login_url='login')
def ProfileUpdateView(request):
    form = UserUpdateForm(request.POST or None, instance=request.user)
    form_profile = ProfileForm(request.POST or None,
                               instance=request.user.profile, files=request.FILES or None)
    
    print(request.user.profile.first_join)

    if not request.user.profile.first_join and not '?edit' in request.get_full_path():
        return redirect('dashboard')

    if request.user.profile.first_join:
        request.user.profile.first_join = False
        request.user.profile.save()

    if request.method == 'POST' and form_profile.is_valid() and form.is_valid():

        form.save()
        form_profile.save()
        messages.success(request, 'Perfil actualizado correctamente')
    elif request.method == 'POST':
        messages.error(request, 'Error al actualizar el perfil')

    return render(request, 'registration/profile_form.html', {'form_profile': form_profile, 'form': form})
