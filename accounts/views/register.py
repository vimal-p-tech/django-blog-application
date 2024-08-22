from typing import Any
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.http import HttpResponse
from ..forms import RegistrationForm
from django.contrib import messages

# Create your views here.


class RegisterView(FormView):
    
    initial        = {}
    form_class     = RegistrationForm
    success_url    = reverse_lazy('blog:index_blogs')
    template_name  = "accounts/signup.html"

    def set_form_attributes(self,form):
       form.method = 'POST'
       form.action = '.'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        self.set_form_attributes(kwargs['form'])
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Registration successful. Please login.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)




