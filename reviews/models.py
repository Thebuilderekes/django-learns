from django.conf import settings
from django.db import models


class Publisher(models.Model):
    """A company that publishes books."""

    name = models.CharField(
        max_length=50,
        help_text="The name of the Publisher.",
        db_index=True  # Index for faster lookups
    )
    website = models.URLField(help_text="The publisher's website")
    email = models.EmailField(help_text="The publisher's email")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """A contributor to a book, e.g author, editor, co-author"""

    first_names = models.CharField(
        max_length=50,
        help_text="First name of contributor"
    )
    last_names = models.CharField(
        max_length=50,
        help_text="Last name of contributor",
        db_index=True  # Index for searching by last name
    )
    email = models.EmailField(help_text="The contributor's email")
    id = models.AutoField(primary_key=True)
    class Meta:
        ordering = ['last_names', 'first_names']
        indexes = [
            models.Index(fields=['last_names', 'first_names']),
        ]

    def __str__(self):
        return f"{self.first_names} {self.last_names}"

    @property
    def full_name(self):
        """Returns the contributor's full name."""
        return f"{self.first_names} {self.last_names}"


class Book(models.Model):
    """
    Represents a book with its publication details.

    Links to Publisher (one-to-many) and Contributors (many-to-many).
    """

    title = models.CharField(
        max_length=70,  # Increased for longer titles
        help_text="The title of the book",
        db_index=True  # Index for searching books by title
    )
    publication_date = models.DateField(
        verbose_name="Publication date",
        db_index=True  # Index for filtering by date
    )
    isbn = models.CharField(
        max_length=20,
        verbose_name="ISBN",
        unique=True,  # ISBNs should be unique
        db_index=True
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books'  # Access publisher's books via publisher.books.all()
    )
    contributors = models.ManyToManyField(
        Contributor,
        through="BookContributor",
        related_name='books'  # Access contributor's books via contributor.books.all()
    )

    class Meta:
        ordering = ['-publication_date', 'title']
        indexes = [
            models.Index(fields=['title', 'publication_date']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        return self.title

    def get_average_rating(self):
        """Calculate the average rating for this book."""
        from django.db.models import Avg
        result = self.reviews.aggregate(avg_rating=Avg('rating')) # type: ignore
        return result['avg_rating'] or 0


class BookContributor(models.Model):
    """
    A model that links a Book to a Contributor, specifying the
    contributor's role.

    This is a "through" table used to manage the many-to-many relationship
    between books and contributors, allowing us to store extra information,
    like the specific role (e.g., Author, Editor), on the relationship itself.
    """

    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book_contributors'
    )
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name='book_contributions'
    )
    role = models.CharField(
        verbose_name="Role",
        choices=ContributionRole.choices,
        max_length=20,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'contributor', 'role'],
                name='unique_book_contributor_role'
            ),
        ]
        ordering = ['role', 'contributor__last_names']
        indexes = [
            models.Index(fields=['book', 'role']),
        ]

    def __str__(self):
        return f"{self.contributor.full_name} - {self.get_role_display()} - {self.book.title}" #type: ignore[attr-defined]  # type: ignore[attr-defined]

class Review(models.Model):
    """
    Represents a single user's review and rating for a specific book.

    This model stores all the essential information for a book review,
    including the book it's for, the user who wrote it, the rating they
    gave, and the review's text and timestamps.
    """

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',  # Access book reviews via book.reviews.all()
        help_text="The book that this review is for"
    )
    content = models.TextField(
        help_text="Provide a detailed review of the book.",
        blank=True  # Make optional at model level
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Better than auth.get_user_model()
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        help_text="The rating that the reviewer has given (1-5)",
        choices=[(i, i) for i in range(1, 6)]  # Limit to 1-5 range
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time the review was created"
    )
    date_edited = models.DateTimeField(
        auto_now=True,  # Automatically update on save
        help_text="Date and time the review was last edited"
    )

    class Meta:
        ordering = ['-date_created']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'creator'],
                name='unique_book_creator'
            ),
        ]
        indexes = [
            models.Index(fields=['book', '-date_created']),
            models.Index(fields=['creator', '-date_created']),
            models.Index(fields=['-rating']),  # For getting top-rated reviews
        ]

    def __str__(self):
        return f"Review of '{self.book.title}' by {self.creator.username}"

    def save(self, *args, **kwargs):
        """Validate rating before saving."""
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        super().save(*args, **kwargs)
