from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView, TemplateView

from siteauth.forms import UserForm, RegistrationForm


User = get_user_model()


class LoginView(FormView):
    form_class = UserForm
    success_url = reverse_lazy('home')
    template_name = 'auth/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('/')


class SignUpView(LoginRequiredMixin, CreateView):
    """Sign Up view is closed temporariliy
    """
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    form_class = RegistrationForm
    model = User
    success_url = reverse_lazy('home')
    template_name = 'auth/signup.html'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('username'))
        if user:
            login(self.request, user)
        return super().form_valid(form)
