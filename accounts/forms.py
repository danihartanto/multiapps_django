from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, ResetPasswordKeyForm
from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            css_class = field.widget.attrs.get('class', '')
            # tambahkan form-control kalau belum ada
            if 'form-control' not in css_class:
                field.widget.attrs['class'] = (css_class + ' form-control').strip()



class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class MyLoginForm(BootstrapMixin, LoginForm):
    pass

class MySignupForm(BootstrapMixin, SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class MyResetPasswordForm(BootstrapMixin, ResetPasswordForm):
    pass

class MyResetPasswordKeyForm(BootstrapMixin, ResetPasswordKeyForm):
    pass
