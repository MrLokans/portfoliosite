from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import TemplateView, View, FormView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.urlresolvers import reverse_lazy

from .forms import FlatPageForm
from blog.models import Post
from blog.forms import UserForm, RegistrationForm
from books.models import Book


User = get_user_model()


class HomeView(TemplateView):

    def get(self, request):
        form = FlatPageForm()
        posts = Post.objects.all()
        context = {'posts': posts, 'new_post_form': form}
        return render(request, "home.html", context)


class AboutMeView(TemplateView):

    def get(self, request):
        return render(request, "about_me.html")


class NewPost(View):

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        user = request.user
        content = request.POST['content']

        post = Post(author=user, content=content)
        post.save()
        return redirect('/')


class ProjectView(TemplateView):

    def get(self, request):
        return render(request, "projects.html")


class LoginView(FormView):
    form_class = UserForm
    success_url = reverse_lazy('home')
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        print(username, password)
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


class SignUpView(CreateView):
    form_class = RegistrationForm
    model = User
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('username'))
        if user:
            login(self.request, user)
        return super().form_valid(form)
