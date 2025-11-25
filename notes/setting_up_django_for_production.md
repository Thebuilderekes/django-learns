## How to start a new Django project and prepare for production
`django-admin startproject projectname`
`cd projectname`
`python manage.py startapp appname`

- Make sure your templates DIR is properly referred to in the settings and the url
matches where the template is located
- Make sure your views exist and the `urls.py` file is properly mapped to the
  right view
- STATIC_URL has to be changed to fit the link of where your website is hosted

You have to test production conditions by using `collectstatic` to serve your static files, setting the STATIC_ROOT location for the collect static folder  and setting `DEBUG=False` as this is what will be expected by the server you will be using in production.

