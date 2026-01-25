from django.contrib.admin.apps import AdminConfig
# This class is used to define the application that should be used as a default admin site, and also to override the default behavior of the Django admin site.
# this connects to the BookrAdmin class in admin.py
class BookrAdminConfig(AdminConfig):
    default_site = 'bookr_admin.admin.BookrAdmin'



# This came with the creation of book_admin app and had to be overridden with the custom bookrAdmin above
# from django.apps import AppConfig
#
#
# class BookrAdminConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "bookr_admin"
