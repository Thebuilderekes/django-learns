# from django.contrib import admin
from django.urls import path
from .views import index, media_example, file_upload_form, success

urlpatterns = [
    path("", index, name="index"),
    path("media_upload/", media_example, name="media_upload"),
    path("create_upload/", file_upload_form, name="create_upload"),
    path('success/', success, name='success'),

]
