for post in post_queryset:
    # Use the __str__ method (if defined in models.py)
    # Access specific fields directly
    print(f"ID: {post.id}")
    print(f"Slug: {post.slug}")
    print(f"Published Date: {post.publish_date}")
    print(f"Author ID: {post.author_id}")
    print("-" * 20)
