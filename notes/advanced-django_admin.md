## Advanced admin - creating custom admin site
- We use ``python3 manage.py startapp Bookr_admin`` inside bookr directory to
create a new app to control our custom bookr admin site class in the admin.py file and redirect out url patterns to it to be our new admin_site
- We want to make out custom admin site useful for our users so we will register
out User model from auth to make it work with it.. Doing this allow us access
to the Users in the admin site at ``/myadmin`` Without registering users, we
will not have permission to make any changes at ``/myadmin`` even after logging in
- Check the site_header if it matches with what we set in thje `admin.py` file,
this is how you know that you are using the right admin_site that you created
- We then need to create a custom `AdminConfig` class that overrides the content of the
``apps.py`` file that comes with the creation of out custom `bookr_admin` app
This class is used to define the application that should be used as a default admin site,
and also to override the default behavior of the Django admin site.
- We include the `"bookr_admin.apps.BookrAdminConfig",` into ``settings.py file``
under installed apps

## Customizing templates
`{% extends "admin/base_site.html" %}` is what maintains the base layout of our
dashboard so all our templates that we are going to be Customizing has to have this at the top

