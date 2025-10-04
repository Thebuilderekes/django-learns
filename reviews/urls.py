from django.urls import path
from django.contrib import admin
from . import views
#from .admin import admin_site
# change back to above if it does not work

urlpatterns = [
    #path("admin/", admin_site.urls),
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("books/", views.book_list),
    path("book-search/", views.book_search),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("test/", views.test_page),
]
