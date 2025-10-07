from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from reviews.models import Book, Review, Contributor, BookContributor, Publisher

from .site import admin_site
from .book import BookAdmin
from .publisher import PublisherAdmin
from .contributor import ContributorAdmin
from .review import ReviewAdmin
from .book_contributor import BookContributorAdmin


# Register models to the custom admin site
# this is the admin_site.urls that is pointed to in the mysite.urls.py file
admin_site.register(Book, BookAdmin)
admin_site.register(Contributor, ContributorAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(BookContributor, BookContributorAdmin)
admin_site.register(Publisher, PublisherAdmin)

# Register Django's default auth models
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
