from django.shortcuts import render,  get_object_or_404
from blog.models import Post


def post_list(request):
    published_posts= Post.published.all()
    # published.all is from the manager that was created to handle published posts
    context = {
        'published_posts':published_posts
    }
    """displays index page"""
    return render(request, "blog/posts/post_list.html", context)
# Assuming 'published' is the status value for published posts

def post_detail(request, year, day, month, post):
    post = get_object_or_404(
        Post,
        publish_date__year = year,
        publish_date__day = day,
        publish_date__month = month,
        slug=post,
    )
    post.body = "ekeopre is creating a blog that allows for creating blog posts that others can comment on"
    post.save()
    print("this is post", post)
    return render(request, 'blog/posts/post_detail.html', {'post': post})
