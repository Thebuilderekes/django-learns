from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/<int:post_id>/share/", views.post_share, name = "post_share"),
    path(
        "posts/<int:year>/<int:day>/<int:month>/<slug:post>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
]
