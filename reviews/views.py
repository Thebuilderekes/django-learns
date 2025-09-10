from django.http import HttpResponse

# views.py
def blog_home(request):
    return HttpResponse("Welcome to the blog in review!")

# Create your views here.
