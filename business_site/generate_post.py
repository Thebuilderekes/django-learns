import random
from django.utils import timezone
from blog.models import Post
from django.contrib.auth import get_user_model
# --- Configuration ---
NUM_POSTS = 20
User = get_user_model()
try:
    # 1. Get the first superuser or a random user to assign as the author
    author = User.objects.filter(is_superuser=True).first() or User.objects.first()
    if not author:
        print("ERROR: Cannot find a user. Please create one user first.")
except Exception as e:
    print(f"Error accessing users: {e}")
    author = None

# --- Data Generation Logic ---
if author:
    statuses = [Post.Status.DRAFT, Post.Status.PUBLISHED]

    for i in range(1, NUM_POSTS + 1):
        # Determine Status and Title
        status_choice = random.choice(statuses)
        title = f"Random Post #{i}: {status_choice.capitalize()}"
        slug = f"random-post-{i}-{status_choice.lower()}"

        # Determine Publish Date (use current time for simplicity)
        publish_date = timezone.now()

        # Create and Save the Post
        Post.objects.create(
            title=title,
            slug=slug,
            author=author,
            # Assigning the correct date to your field: publishe_date
            publishe_date=publish_date,
            status=status_choice,
            body=f"This is the body text for post number {i}. Its current status is {status_choice}."
        )
        print(f"Created Post {i}: Title='{title}' | Status='{status_choice}'")

    print(f"\n--- SUCCESS: {NUM_POSTS} posts generated and saved to the database. ---")
