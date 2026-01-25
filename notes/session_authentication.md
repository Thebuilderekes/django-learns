## Middleware
Middleware is a framework of hooks into Django’s request/response
processing. It’s a light, low-level “plugin” system for globally altering
Django’s input or output.

The two important aspects of stateful application development that are
implemented as middleware components – SessionMiddleware and
AuthenticationMiddleware. The process_request method of SessionMiddleware adds a
session object as an attribute of the request object. The process_request method
of AuthenticationMiddleware adds a user object as an attribute of the request
object.



## Setting up class based views for login, logout, password_reset, password_change  etc
- We used the ``django.contrib.auth.urls`` with the `accounts` namespace to setup the views that Django
already has to speed up the process.
- The accounts/profile/ page is setup to display after user has been
authenticated.
- The navigation link for login and logout are setup to display with
conditionals checking if ``user.is_authenticated``


## Sessions
A session refers to a user's current interaction with a web server or application and
requires that data is persisted for the duration of the interaction. This may
include information about the links that the user has visited, the actions that
they have performed, and the preferences that they have made in their
interactions.
- Session support is activated by default in Django
- By default in Django session information is stored in the project's database.
-




## Setting up permission

It is best to give permission to groups when setting up authentication.
