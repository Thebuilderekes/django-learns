from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("media_project/", include("media_project.urls", namespace='media_project')),

]
