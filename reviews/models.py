from django.contrib import auth
from django.db import models


# Create your models here.
class Publisher(models.Model):
    """A company that publishes books."""

    # Publisher class is a subclass of Django's models.Model
    # having attributes like name, website and email
    # Every model field takes in a default value in this case it is set as help_text
    name = models.CharField(max_length=50, help_text="The name of the Publisher.")
    website = models.URLField(help_text="The publisher's website")
    email = models.EmailField(help_text="The publisher's email")

    def __str__(self):
        return str(self.name)


class Contributor(models.Model):
    """A contributor to a book, e.g author, editor, co-author"""

    first_names = models.CharField(max_length=50, help_text="first name of contributor")
    last_names = models.CharField(max_length=50, help_text="last name of contributor")
    email = models.EmailField(help_text="The publisher's email")

    def __str__(self):
        return f"{self.first_names}"


class Book(models.Model):
    """defining a book model"""

    title = models.CharField(
        max_length=50, help_text="The name of the Publisher.cation_dates"
    )
    publication_date = models.DateField(verbose_name="saye book was published")
    isbn = models.CharField(max_length=20, verbose_name="ISBN of the book")
    # we will now refer to the table that we want to associate a
    # book to so the one is Publisher, the many is Book
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributor = models.ManyToManyField(Contributor, through="BookContributor")

    def __str__(self):
        return f"{self.title}"


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    contributor = models.ForeignKey("Contributor", on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this contributor had in the book.",
        choices=ContributionRole.choices,
        max_length=20,
    )

    def __str__(self):
        return f"{self.contributor} - {self.book}"
        # • book: This is a foreign key to the Book model.
        # As we saw previously, on_ delete=models.CASCADE will delete an
        # entry from the relationship table when the relevant book is deleted from the application.
        # • Contributor: This is again a foreign key to the
        # Contributor model/table. This is also defined as CASCADE upon deletion.
        # • role: This is the field of the intermediary model,
        # which stores the extra information about the relationship between Book and Contributor.
        # • class ContributionRole(models.TextChoices): This can be used to define a set of 
        #choices by creating a subclass of models.TextChoices. For example, 
        #ContributionRole is a subclass created out of TextChoices, which is used by 
        # the roles field to define Author, Co-Author, and Editor as a set of choices.
        # • choices: This refers to a set of choices defined in the models, and they are useful when creating Django Forms using the models.


# The Review model to store user-submitted reviews and ratings.
class Review(models.Model):
    """
    Model to store a single user's review and rating for a specific book.
    """

    # A foreign key to the Book model, creating a many-to-one relationship.
    # When a book is deleted, all its reviews will also be deleted (CASCADE).
    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, help_text="The book that this review is for"
    )

    # A text field for the review comment. It is optional.
    comment = models.TextField(help_text="Provide a detailed review of the book.")

    # A foreign key to the User model provided by Django's authentication system.
    # When a user is deleted, their reviews are also deleted.
    user = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
    )

    # An integer field for the rating, with validators to ensure it's between 1 and 5.
    rating = models.IntegerField(help_text="the rating this user ghas given")

    # A timestamp for when the review was created.
    # auto_now_add=True automatically sets the date and time when the object is first created.
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="date and time the review was created"
    )
    # A timestamp for when the review was edited
    date_edited = models.DateTimeField(
        null=True, help_text="date and time the review was edited"
    )
