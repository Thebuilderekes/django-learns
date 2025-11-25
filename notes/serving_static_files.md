## Static files serving
Django has a built-in feature that can serve static files (like images, CSS, or JavaScript) while you’re developing your website.

However, in a production (live) environment, Django should not serve these static files. That’s not what it’s designed for.

In production, you should let a regular web server (like Nginx or Apache) handle static files instead because:

Those servers are faster at sending files.

If Django handles static files, it keeps your Python code busy doing simple file transfers instead of processing the more complex, dynamic parts of your website (like database queries or user interactions).

So, in short:
👉 Use Django’s static file serving only for development.
👉 Use a real web server to serve static files in production.

 ## Serving files using `collectstatic` command



## IMPORTANT
`` STATICFILES_DIRS`` can be used to handle multiple static files in the settings. In situation  where there is a global static file that needs to be accessed, all that would be needed is to list it in the STATIC_DIRS list in settings. 

Now with the files in the `STATICFILES_DIRS`list set in `settings.py``, If you had a CSS file you wanted to serve globally, you can create a static folder with `global.css`.as a file inside of then you can use 
`{% static 'global.css' %}` to serve the style sheet in any of the templates in the app

!**NOTE**
The first instance of a static file as found in the `STATICFILES_DIRS` list is the one that will be loaded


 ## The static/
The ``static/`` is a view in itself that has been automatically setup in `urls.py` by
Django because it is in the installed apps
The URL mapping that is created is roughly equivalent to having the following map in your urlpatterns: ``path(settings.STATIC_URL, django.conf.urls.static)``

STATIC_URL has to be changed to fit the link of where your website is hosted
when you want to serve in production

## static file Namespacing
t is common convention to have ``app/static/app/style.css`` as a pattern of naming to be able to distinguish static files from each other across different apps. You can also do ``main/app/static/main.app/style.css`` 

## `findstatic command`
`findstatic` command is used to find a static file,  especially when the file has not been namespaced
`pythonmanage.py findstatic filename`

You can find multiple files like
`pythonmanage.py findstatic filename1 filename2`

You can also use the command with verbosity levels to get more info about how it is looking for the files
`pythonmanage.py findstatic -v0/-v1/-v2 filename1 filename2` this is for either -v or -v2 or v3 level of verbosity


## ManifestFilesStorage
`ManifestFilesStorage` is a way to provide hashing of filenames to files after `collectstatic` so that files can be tracked to know when a file has been modified

## Custom Storage Engines 
In the previous section, we set the storage engine to ``ManifestFilesStorage``. This class is provided by Django, but it is also possible to write a custom storage engine. For example, you could write a storage engine that uploads your static files to different backend services like s3, 


Django-storages allow for custom static file uploads


## cache invalidation
