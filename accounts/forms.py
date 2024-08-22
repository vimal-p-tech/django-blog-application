from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(self.__class__,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['password'].widget.attrs.update({'class':'form-control'})


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.required_list:
            self.fields[field].required = True
 
    required_list = ['username','first_name','last_name','email']
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':'password'}),
    )
    
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Firstname', 'class': 'form-control','required':'required'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Lastname', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Apply custom validators
        from .validators import validate_username_length,validate_username_characters
        from django.core.exceptions import ValidationError
        validate_username_length(username)
        validate_username_characters(username)

        # Check for uniqueness
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')

        return username
