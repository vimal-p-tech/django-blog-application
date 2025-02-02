
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth import (
        REDIRECT_FIELD_NAME,
        login,
        logout,
        get_user_model,
        update_session_auth_hash
    )

from django.contrib.auth.views import LoginView,LogoutView
from ..forms import LoginForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


class PheonixLoginView(LoginView):
    redirect_field_name         = REDIRECT_FIELD_NAME
    success_url                 = reverse_lazy('blog:dashboard')
    template_name               = "accounts/login/login.html"
    authentication_form         = LoginForm
    

    def get_context_data(self, **kwargs):
        kwargs  = super().get_context_data(**kwargs)

        kwargs['form'].method  = 'POST'
        kwargs['form'].action  = '.'
        kwargs['form'].title   = 'Login'

        return kwargs
    
    def get_success_url(self):
        return super().get_success_url()
    
class PheonixLogout(LogoutView):
    ...

    
