from django.db import models

class Publisher(models.Model):
    """A company that publishes books."""

    # Publisher class is a subclass of Django's models.Model
    # having attributes like name, website and email
    # Every model field takes in a default value in this case it is set as help_text
    name = models.CharField(max_length=50, help_text="The name of the Publisher.")
    website = models.URLField(help_text="The publisher's website")
    email = models.EmailField(help_text="The publisher's email")

class Contributor(models.Model):
    """A contributor to a book, e.g author, editor, co-author"""
    first_names = models.CharField(max_length=50, help_text = "first name of contributor")
    last_names = models.CharField(max_length=50, help_text = "last name of contributor")
    email = models.EmailField(help_text="The publisher's email")



    # Create your models here.
class Book(models.Model):

    name = models.CharField(max_length=50, help_text="The name of the Publisher.cation_dates")
    publication_date = models.DateField(verbose_name = 'saye book was published')
    isbn = models.CharField(max_length=20, verbose_name = 'ISBN of the book')
    #we will now refer to the table that we want to associate a 
    #book to so the one is Publisher, the many is Book
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributor = models.ManyToManyField(Contributor, through="BookContributor")

class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    contributor = models.ForeignKey('Contributor', on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this contributor had in the book.",
        choices=ContributionRole.choices,
        max_length=20
    )

    def __str__(self):
        return f"{self.contributor} - {self.book}"
