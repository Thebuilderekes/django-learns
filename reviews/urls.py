from django.urls import path

# from django.contrib import admin
from . import views

# from .admin import admin_site
# change back to above if it does not work

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("books/", views.book_list),
    path("books/<int:pk>/media/", views.book_media, name="book_media"),
    path(
        "book/<int:book_pk>/review/<int:review_pk>/edit/",
        views.review_edit,
        name="review_edit",
    ),
    path("books/create_book/", views.book_create_edit, name="book_create_edit"),
    path("search-result/", views.search_result, name="search_result"),
    path("book-search/", views.book_search, name="book_search"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    # path("publisher-edit/", views.publisher_edit,name="publisher_edit"),
    path("publishers/", views.publisher_list, name="publisher_list"),
    path("publishers/create/", views.publisher_create_edit, name="publisher_create"),
    path("publishers/<int:pk>/", views.publisher_detail, name="publisher_detail"),
    path(
        "publishers/<int:pk>/edit/", views.publisher_create_edit, name="publisher_edit"
    ),
]
