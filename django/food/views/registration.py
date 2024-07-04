from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from ..forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from ..tokens import account_activation_token
from django.core.mail import EmailMessage
import uuid
from django import forms

class UserRegistrationDoneView(TemplateView):
    template_name = "registration/registration_done.html"

class UserRegistrationFromView(FormView):
    template_name = "registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('food:registration_done')
    
    def form_valid(self, form:UserRegistrationForm):
        user:User = form.instance
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.email = form.cleaned_data["email"]
        user.is_active = False
        user.save()
        
        current_site = get_current_site(self.request)
        pk_bytes = force_bytes(user.pk)
        uid = urlsafe_base64_encode(pk_bytes)
        mail_subject = 'Активируйте свой аккаунт.'
        message = render_to_string('registration/acc_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':uid,
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        
        return super().form_valid(form)
    
class UserLoginFormView(LoginView):
    authentication_form = CustomUserAuthenticationForm
    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        user = User.objects.get(username=form.cleaned_data["username"])
        
        if user and not user.is_active:
            form.errors.clear()
            form.add_error(None, forms.ValidationError("Пользователь не поддтеврдил Email"))
        
        return super().form_invalid(form)
    
class UserActivateView(TemplateView):
    template_name="registration/acc_activated.html"
    def get(self, request, *args, **kwargs):
        try:
            uidb64_str = self.kwargs["uidb64"]
            #uidb64_uuid = uuid.UUID(uidb64_str)
            uid_decode = urlsafe_base64_decode(uidb64_str)
            uid = force_str(uid_decode)
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, self.kwargs["token"]):
            user.is_active = True
            user.save()
            return super().get(request)
        else:
            return HttpResponse('Activation link is invalid!')
        
    
