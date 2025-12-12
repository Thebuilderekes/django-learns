from django.shortcuts import render,  get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import Post
from business_site.settings import POSTS_PER_PAGE

def post_list(request):
    """
        Retrieves all published blog posts using the custom manager.
        It paginates the results using the configured page size (POSTS_PER_PAGE).
        The view fetches the specific page number requested via the URL's '?page=N'
        query parameter and passes the paginated set to the list template.
        Also handle any exceptions
    """
    published_posts= Post.published.all()
    # published.all is from the manager that was created to handle published posts
    paginator = Paginator(published_posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        #if page_number is out of range get last page of results
        paginated_posts = paginator.page(paginator.num_pages)
    context = {
        'posts': paginated_posts
    }
    """displays index page"""
    return render(request, "blog/posts/post_list.html", context)
# Assuming 'published' is the status value for published posts

def post_detail(request, year, day, month, post):
    """
        Handles requests for a single, specific blog post.

        It retrieves the Post object from the database using four parameters
        captured from the URL: Year, Month, Day, and the Post's Slug (post).

        Note: It currently overrides and saves the post's body with a fixed string
        before rendering the detail template.
        """
    post = get_object_or_404(
        Post,
        publish_date__year = year,
        publish_date__day = day,
        publish_date__month = month,
        slug=post,
    )
    print("this is post", post)
    return render(request, 'blog/posts/post_detail.html', {'post': post})
