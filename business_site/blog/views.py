from django.shortcuts import render


def index(request):
    """displays index page"""
    return render(request, "index.html")


# Create your views here.
