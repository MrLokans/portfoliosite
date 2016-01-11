from django.shortcuts import render

from .models import Book


def index(request):
    print("test")
    return render(request, "home.html")


def books(request):
    books = Book.objects.all()
    return render(request, "book.html", {"books": books})


def about_me(request):
    return render(request, "about_me.html")


def projects(request):
    return render(request, "projects.html")
