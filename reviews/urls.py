from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.book_list),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("test/", views.test_page),
]
