from django.contrib import admin

# from reviews.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "date_created", "date_edited")
