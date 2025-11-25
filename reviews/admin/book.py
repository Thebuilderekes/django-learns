from django.contrib import admin

from reviews.models import Book


class BookAdmin(admin.ModelAdmin):
    ## These variables represent components that are displayed under the book model in the admin page
    # date_hierarchy = "publication_date"
    list_display = ("title", "isbn")
    list_filter = ("publisher", "publication_date")
    search_fields = ("title", "isbn", "publisher__name")
