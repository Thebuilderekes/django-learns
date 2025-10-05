from django.contrib import admin
from reviews.models import Book, Review, Contributor, BookContributor, Publisher

class BookRevAdminSite(admin.AdminSite):
    # Set your custom titles and headers here
    site_title = 'BookRev Admin'
    site_header = 'BookRev Administration'
    index_title = 'BookRev Site Administration'

class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn')
    list_filter = ('publisher', 'publication_date')

# This will be automatically created by AdminConfig
# But we also create it here for use in urls.py
admin_site = BookRevAdminSite(name='bookrevadmin')

# Register models to the custom admin site
admin_site.register(Book, BookAdmin)
admin_site.register(Contributor)
admin_site.register(Review)
admin_site.register(BookContributor)
admin_site.register(Publisher)

# Register Django's default auth models (imported here to avoid circular import)
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

