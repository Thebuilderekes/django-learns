from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "form_submit/",
        TemplateView.as_view(template_name="form_submit.html"),
        name="form_submit",
    ),
]
