from django.contrib import admin
from reviews.models import Book, Review, Contributor, BookContributor, Publisher

class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn')
    list_filter = ('publisher', 'publication_date')


admin.site.register(Book)
admin.site.register(Contributor)
admin.site.register(Review)
admin.site.register(BookContributor)
admin.site.register(Publisher)

# Register your models here.

