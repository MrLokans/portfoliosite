from django.views.generic import TemplateView
from django.views.generic.list import ListView

from django.shortcuts import render, redirect

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
        print("POST DATA: {}".format(request.POST))
        username = request.POST['username']
        password = request.POST['password']

        return redirect('/')


class LogoutView(TemplateView):

    def get(self, request):
        pass


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
