from django.shortcuts import render,  get_object_or_404
from blog.models import Post


def post_list(request):
    posts= Post.published.all()
    # published.all is from the manager that was created to handle published posts
    context = {
        'posts': posts
    }
    """displays index page"""
    return render(request, "blog/posts/post_list.html", context)
# Assuming 'published' is the status value for published posts

def post_detail(request, id):
    post = get_object_or_404(
        Post,
        id=id,
    )
    print("this is post", post)
    return render(request, 'blog/posts/post_detail.html', {'post': post})
