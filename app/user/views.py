import logging

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import AuthenticationForm
from .forms import UserCreationForm


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('articles:main')
    template_name = 'user/register.html'

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        return super().form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('articles:main')
    template_name = 'user/login.html'

    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


class LoginOAuthView(FormView):
    """Получение OAuth токена"""
    success_url = reverse_lazy('home')
    template_name = 'article/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        response = requests.post(settings.URL_PREFIX_OAUTH_SERVER + '/o/token/',
                                 data={'grant_type': 'password',
                                       'username': form.cleaned_data['username'],
                                       'password': form.cleaned_data['password']},
                                 auth=(settings.CLIENT_ID, settings.CLIENT_SECRET))
        if response.status_code == 200:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


def token_auth_view(request, key):
    logger = logging.getLogger('connexio')
    user = authenticate(key=key)
    if user:
        login(request, user, backend='user.backends.UrlTokenBackend')
    else:
        logger.warning(f'Пользователь не аутентифицирован {key}')

    next_url = request.GET.get('next', reverse_lazy('admin:index'))

    return HttpResponseRedirect(next_url)
