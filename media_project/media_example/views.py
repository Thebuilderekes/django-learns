from django.shortcuts import redirect, render
import os
from django.conf import settings
from .models import Hotel
from .forms import HotelForm


def index(request):
    welcome_message = "welcome to media app"
    context = {
        "message": welcome_message
    }
    return render(request, "media_example/index.html", context)


def media_example(request):
    if request.method == 'POST':
        save_path = os.path.join(settings.MEDIA_ROOT, request.FILES["file_upload"].name)
        with open(save_path, "wb") as output_file:
            for chunk in request.FILES["file_upload"].chunks():
                output_file.write(chunk)
    return render(request, "media_example/media-example.html")


from django.http import HttpResponse

def file_upload_form(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HotelForm()
    return render(request, 'media_example/template.html', {'form': form})

def success(request):
    return HttpResponse('Successfully uploaded!')
