from django.shortcuts import render


def index(request):
    print("test")
    return render(request, "home.html")
