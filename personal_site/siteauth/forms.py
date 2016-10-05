from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, ButtonHolder, HTML


User = get_user_model()


class UserForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.form_class = 'form-signin'
        self.help_text_inline = True
        self.helper.layout = Layout(
            HTML('<h2 class="form-signin-heading">Please sign in</h2>'),
            Field('username', placeholder='Username'),
            Field('password', placeholder='Password'),
            'remember_me',
            ButtonHolder(
                Submit('login', 'Login',
                       css_class='btn btn-lg btn-primary btn-block')
            )
        )

    username = forms.CharField(label="")
    password = forms.CharField(widget=forms.PasswordInput(), label="")
    remember_me = forms.BooleanField(required=False)

    def clean_remember_me(self):
        """clean method for remember_me """
        remember_me = self.cleaned_data.get('remember_me')
        if not remember_me:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
        else:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        return remember_me

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h2 class="form-signin-heading">Please sign in</h2>'),
            Field('username', placeholder='Username'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Repeat password'),
            'remember_me',
            ButtonHolder(
                Submit('register', 'Register',
                       css_class='btn btn-lg btn-primary btn-block')
            )
        )

    remember_me = forms.BooleanField(required=False)
    username = forms.CharField(label="")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="")
