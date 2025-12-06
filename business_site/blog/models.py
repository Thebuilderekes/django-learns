from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    # Every post has 2 states draft or published,
    # the Status class is to track these states
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        published = 'PB', 'published'

    title = models.CharField(
            max_length=250,  # Increased for longer titles
            help_text="The title of the post",
            db_index=True  # Index for searching  post title
        )
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )

    published = models.DateTimeField(
        default=timezone.now
        )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default = Status.DRAFT
    )

    body = models.TextField(
            help_text="Provide a body of the post.",
            blank=True  # Make optional at model level
    )

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published'])
        ]
    def __str__(self):
        return self.title
