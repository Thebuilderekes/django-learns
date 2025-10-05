"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from reviews.admin import admin_site

# NOte that you can import reviews.views and
# individually use each url directly in this file but for
# organization the entire reviews url is included in the file
urlpatterns = [
    path('admin/', admin_site.urls),
    path("", include("reviews.urls")),
    # This maps to reviews/urls.py to get to the view.py
    # that accesses the index function to then render the view in
    # the browser at localhost:8000 path. To get it to render at /review
    # simply change the path to "reviewsa"
]
