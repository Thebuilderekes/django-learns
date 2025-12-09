from django.urls import path
from django.views.generic import TemplateView
from . import views
app_name = 'blog'

urlpatterns = [
    path("posts/list/", views.post_list, name='post_list' ),
        path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path("about/", TemplateView.as_view(template_name='index.html'),  name='about' ),
]
