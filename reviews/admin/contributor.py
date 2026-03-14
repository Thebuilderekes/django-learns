from django.contrib import admin

# from reviews.models import BookContributor

# class BookContributorInline(admin.TabularInline):
#     model = BookContributor
#     extra = 1  # Number of

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_names', 'first_names', 'email')
    search_fields = ('last_names', 'first_names', 'email')
    # You can also see all books a person worked on from their page:
    # inlines = [BookContributorInline]
