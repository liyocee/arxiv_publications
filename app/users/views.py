from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        form.save()
        return redirect('users:login')


class UserLoginView(LoginView):
    template_name = 'users/login.html'
