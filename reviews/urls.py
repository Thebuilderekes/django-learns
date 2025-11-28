from django.urls import path

# from django.contrib import admin
from . import views

# from .admin import admin_site
# change back to above if it does not work

urlpatterns = [
    # path("admin/", admin_site.urls),
    # path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("books/", views.book_list),
   # path("publisher-edit/", views.publisher_edit,name="publisher_edit"),
    path("publisher-edit/<int:pk>/", views.publisher_edit, name="publisher_edit"),
    # 2. CREATE ROUTE (For accessing the empty form initially)
    # We rename the old static route for clarity (e.g., 'publisher-create')
    path("publisher-new/", views.publisher_edit, name="publisher_create"),
    path("publisher-create/", views.publisher_edit, name="publisher_create"),
    path("post_review/", views.post_review, name="post_review"),
    path("create_review/", views.create_review, name="create_review"),
    path("search-result/", views.search_result, name="search_result"),
    path("book-search/", views.book_search, name="book_search"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
]
