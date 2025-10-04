from django.contrib import auth
from django.db import models


# Create your models here.
class Publisher(models.Model):
# Create your models here.
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
    """creates a Book table in a database with columns for title, publication
    date, ISBN, a link to a publisher, and a link to a list of
        contributors."""
 
    title = models.CharField(max_length=50, help_text="The title of the book")
    publication_date = models.DateField(verbose_name="The date book was published")
    isbn = models.CharField(max_length=20, verbose_name="ISBN of the book")
    # we will now refer to the table that we want to associate a
    # book to so the one is Publisher, the many is Book
    #foreign keys are always set on the many side of the one-to-many relationship
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributor = models.ManyToManyField(Contributor, through="BookContributor")


    def __str__(self):
        return f"{self.title}"


class BookContributor(models.Model):
    """
    A model that links a Book to a Contributor, specifying the
    contributor's role.

    This is a "through" table used to manage the many-to-many relationship
    between books and contributors, allowing us to store extra information,
    like the specific role (e.g., Author, Editor), on the relationship itself.

    Attributes:
        book (ForeignKey): The book associated with the contributor.
        contributor (ForeignKey): The contributor (e.g., author) linked to the book.
        role (CharField): The specific role the contributor had in the book, chosen
                          from a predefined list.
    """

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


class Review(models.Model):
    """
    Represents a single user's review and rating for a specific book.

    This model stores all the essential information for a book review,
    including the book it's for, the user who wrote it, the rating they
    gave, and the review's text and timestamps.

    Attributes:
        book (ForeignKey): The specific book that is being reviewed.
                           Deleting the book will also delete this review.
        user (ForeignKey): The user who submitted the review. Deleting
                           the user will also delete this review.
        rating (IntegerField): The numerical rating given to the book,
                               typically from 1 to 5.
        comment (TextField, optional): The detailed review text provided
                                       by the user.
        date_created (DateTimeField): Automatically set timestamp for
                                      when the review was first created.
        date_edited (DateTimeField, optional): Timestamp for when the
                                               review was last edited.
    """

    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, help_text="The book that this review is for"
    )

    # A text field for the review comment. It is optional.
    content = models.TextField(help_text="Provide a detailed review of the book.")

    # A foreign key to the User model provided by Django's authentication system.
    # When a user is deleted, their reviews are also deleted.
    creator = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(help_text="The rating that the reviewvwer has given")  # Make sure the 'rating' field exists

    # A timestamp for when the review was created.
    # auto_now_add=True automatically sets the date and time when the object is first created.
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="date and time the review was created"
    )
    # A timestamp for when the review was edited
    date_edited = models.DateTimeField(
        null=True, help_text="date and time the review was edited"
    )
