from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import TemplateView, View


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import FlatPageForm
from blog.models import Post
from books.models import Book


class HomeView(TemplateView):

    def get(self, request):
        form = FlatPageForm()
        posts = Post.objects.all()
        return render(request, "home.html", {'posts': posts, 'new_post_form': form})


class AboutMeView(TemplateView):

    def get(self, request):
        return render(request, "about_me.html")


class NewPost(View):

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        user = request.user
        content = request.POST['content']

        post = Post(author=user, text=content)
        post.save()
        return redirect('/')


class ProjectView(TemplateView):

    def get(self, request):
        return render(request, "projects.html")


class LoginView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login')
        else:
            print("Given user does not exist.")


class LogoutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('/')


class SignUpView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')

    def post(self, request, *args, **kwargs):
        pass
