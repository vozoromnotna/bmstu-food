from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from ..forms import UserRegistrationForm, CustomUserAuthenticationForm

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
        user.save()
        return super().form_valid(form)
    
class UserLoginFormView(LoginView):
    authentication_form = CustomUserAuthenticationForm