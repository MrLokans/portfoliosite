from django.views.generic import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):

    def get(self, request):
        return render(request, "home.html")


class AboutMeView(TemplateView):

    def get(self, request):
        return render(request, "about_me.html")


class ProjectView(TemplateView):

    def get(self, request):
        return render(request, "projects.html")
