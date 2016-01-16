from django.views.generic import TemplateView
from django.shortcuts import render, redirect


class HomeView(TemplateView):

    def get(self, request):
        return render(request, "home.html")


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
