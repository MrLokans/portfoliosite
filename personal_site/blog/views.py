from django.views.generic import TemplateView
from django.views.generic.list import ListView

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import FlatPageForm
from .models import Book


class HomeView(TemplateView):

    def get(self, request):
        form = FlatPageForm()
        return render(request, "home.html", {'new_post_form': form})


class AboutMeView(TemplateView):

    def get(self, request):
        return render(request, "about_me.html")


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


class BookListView(ListView):

    model = Book
    context_object_name = 'book_data'
    template_name = 'book_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return Book.non_empty()
