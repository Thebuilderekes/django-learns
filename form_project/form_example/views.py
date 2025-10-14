from django.shortcuts import render
# Create your views def here.
def index(request):
    return render(request, "form_example/index.html" )
