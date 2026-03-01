from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import gettext as _
from reviews.models import Book
from django.template.response import TemplateResponse
from django.urls import path

class BooksAdmin(admin.ModelAdmin):
    model = Book
    list_display = ('title', 'isbn', 'get_publisher')
    search_fields = ['title', 'publisher__name']

    def get_publisher(self, obj):
        return obj.publisher.name
    get_publisher.short_description = _("Publisher")

class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Administration Portal"
    site_title = "Bookr Administration Portal"
    index_title = "Bookr Administration"
    logout_template = 'admin/logout.html'

    def profile_view(self, request):
        request.current_app = self.name
        context = self.each_context(request)
        return TemplateResponse(request, "admin/admin_profile.html", context)

admin_site = BookrAdmin(name='bookr_admin')
admin_site.register(User)
admin_site.register(Book, BooksAdmin)



