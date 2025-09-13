from django.shortcuts import render
from django.http import HttpResponse
# views.py


def index(request):
    """index view for reviews"""
    # name = request.GET.get("name") or "world"
    # say we were working with data in the URL and we look at the query
    # string and find that #there is a blank value set for name like "?name="
    # then the value of name falls to "world"
    context = {"page_name": "reviews", "welcome_message": "Welcome to  Book app"}
    # any variable that need s to be rendered must be passed into the render
    # function as a context as seen below
    return render(request, "reviews/base.html", context)


def search_page(request):
    """search view for search text"""
    search = request.GET.get("search") or "world"
    return HttpResponse(f"{search}")
    #return render(request, "reviews/search.html", search)


# Create your views here.


# Create your views here.
