## ch-1
- Today's exercise is making it so that the ```httpResponse``` displayed on the page
is gotten from the search query result.
- Template directory in settings for allowing templates folder to be read.
- Adding app to installed apps to make sure it is recognized.
- Whitenoise for production file  handling.

## ch-2 Started learning about models and migrations
- ``Makemigration`` and ``migrate`` command after every model creation
- Created models, defined relationships using foreign key and ManytoMany
relations and migrated them.
- Migrations can be rolled back using migrate command and setting it to the
migration code.

## ch-3
- Learned about URL mapping, and how the view works.

## ch-4 learning about Django admin
- Learned about superuser, groups and users.
- Learned about list_display and other model Admin variables and how to use it
to show what details of the model will be on display in columns while viewing it
in the admin page. ManytoMany fields cannot be used in list_display.
- Learned about the various settings that can be applied under a model admin that influences the layout of the model in the admin page.
- Organized the model Admins into their separate folders for maintainability.


## ch-5 serving static file
- Learn about static/ files and how serving them depends on the value of the in STATIC_URL in settings.
- Learned about how to serve files in production environment compared to
- learned about loading static folder into templates to make url paths recognize
from static folder.
- Learned about STATIC_URL and STATIC_ROOT file setting.

##  ch-6 - Advanced form validation
- Learned about how to create form using ``forms.Form``
- Every form field has its own way of getting customized with attributes that
  define the behavior of the field, from required attributes, to character
limits etc.

## Ch-7
- Learned about form validation and what it takes to get validated data from the
  user and sent to the database.

## ch-8
- Learned how to make media work using ```MEDIA_ROOT``` and `MEDIA_URL`
- Learned how to upload files and manipulate how they are stored using the
built-in ``FileField`` and how how to use Pillow library to handled
``ImageField``` class of Django.

## Ch-9 Sessions and authentication



## Advances admin - creating custom admin site and templates
- We use ``python3 manage.py startapp Bookr_admin`` inside bookr directory to
create a new app to control our custom bookr admin site class in the admin.py
file and redirect out url patterns to it to be our new admin_site.
- We created a custom `logout.html`` page with the base html
using `{% extends "admin/base_site.html%}` to keep the layout consistent unless we
choose to create our own html
- Customization like these are important especially when you want to give a particular
page a look and feel that goes with the branding of the website
continue pg 521

