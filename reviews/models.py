from django.db import models


class Publisher(models.Model):
    """A company that publishes books."""

    # Publisher class is a subclass of Django's models.Model
    # having attributes like name, website and email
    # Every model field takes in a deffault value in this case it is set as help_text
    name = models.CharField(max_length=50, help_text="The name of the Publisher.")
    website = models.URLField(help_text="The publisher's website")
    email = models.EmailField(help_text="The publisher's email")

    # Create your models here.
