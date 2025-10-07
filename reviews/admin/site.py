from django.contrib import admin


class BookRevAdminSite(admin.AdminSite):
    # Set your custom titles and headers here
    site_title = 'BookRev Admin'
    site_header = 'BookRev Administration'
    index_title = 'BookRev Site Administration'


# This will be automatically created by AdminConfig
# But we also create it here for use in urls.py
admin_site = BookRevAdminSite(name='bookrevadmin')
