from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone
"""
Defines the Post model for the blog application, including its database fields
(title, slug, body, dates), and relationships (author).

It features a custom manager (`published`) to easily query only posts set
to the 'PUBLISHED' status.

The `get_absolute_url` method generates the canonical URL for a specific post
using its publish date (year/month/day) and slug, enabling easy linking
throughout the site.
"""
class PublishedManager(models.Manager):
    def get_queryset(self):
        return(super().get_queryset().filter(status=Post.Status.PUBLISHED))
## can be return(super().get_queryset().filter(status=self.Status.PUBLISHED))
# using self keyword to make it reusable for any model that needs to use a published status and in that case the Status subclass would be reusable as well, where if used in any model, it would point to that model
#
class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()

    # Every post has 2 states draft or published,
    # the Status class is to track these states
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'published'

    title = models.CharField(
            max_length=250,  # Increased for longer titles
            help_text="The title of the post",
            db_index=True  # Index for searching  post title
        )

    publish_date= models.DateTimeField(
        default=timezone.now,
        )
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
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
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['-publish_date'])
        ]
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish_date.year,
                self.publish_date.day,
                self.publish_date.month,
                self.slug
            ],
        )

class Comment(models.Model):
    post = models.ForeignKey( Post, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)



    class Meta:
        ordering = ['created']
        indexes = [

            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"comment by {self.name} on {self.post}"
