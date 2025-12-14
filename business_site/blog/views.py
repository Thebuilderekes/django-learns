from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from business_site.settings import POSTS_PER_PAGE
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE
    template_name = "blog/posts/post_list.html"

class PostDetailView(DetailView):
    """
    Handles requests for a single, specific blog post using DetailView.
    It retrieves the Post object from the database using year, month, day,
    and slug captured from the URL.
    """
    # 1. Specify the model to work with
    model = Post
    # 2. Specify the template (Django defaults to 'blog/post_detail.html')
    # template_name = 'blog/post_detail.html'
    template_name = 'blog/posts/post_detail.html' # <--- Django uses this
    # 3. Specify the context object name (Django defaults to 'post' or 'object')
    # context_object_name = 'post'
    # 4. Override get_object to handle the complex lookup
    def get_object(self, queryset=None):
        # Retrieve the URL parameters passed from the URLconf
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        post_slug = self.kwargs.get('post')  # The 'post' part is the slug

        # Use get_object_or_404 with the exact same filtering logic
        # as your original function-based view
        post = get_object_or_404(
            Post,
            publish_date__year=year,
            publish_date__month=month,
            publish_date__day=day,
            slug=post_slug,
        )

        # Add the original function's print statement (optional)
        print("this is post", post)

        # NOTE: If you needed to override the body with a fixed string
        # as noted in your docstring, you would do it here before returning:
        # post.body = "A fixed body string for demonstration."
        return post


def post_share(request, post_id):
    """
    Handles the sharing of a blog post via email.

    This view performs the following steps:
    1. Retrieves the published Post object based on the provided post_id.
    2. If the request method is POST (form submission):
       a. Validates the submitted data using EmailPostForm.
       b. If valid, extracts data, composes the email, and sends it.
       c. Renders the 'share' template with a success message (or handles the email failure).
       d. If invalid, re-renders the 'share' template with the form populated
          with submitted data and validation errors.
    3. If the request method is GET (initial load):
       a. Instantiates a blank EmailPostForm.
       b. Renders the 'share' template with the post and the blank form.
    """
    # 1. Retrieve the post
    # Note: Assuming 'Post' and 'EmailPostForm' are correctly imported.
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED # Ensure only published posts can be shared
    )
    sent = False # Flag to indicate if email was sent successfully
    title = f"Share \"{post.title}\" by email"  #page title

    if request.method == 'POST':
        # 2. Form was submitted
        form = EmailPostForm(request.POST)

        if form.is_valid():
            # 2a. Form fields passed validation
            cd = form.cleaned_data

            # Build the URL for the post (Assuming canonical URL is used)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            print(post_url)

            # Compose the email
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )

            # 2b. Send email
            send_mail(subject, message, cd['email'], [cd['to']], fail_silently=False)
            sent = "Message sent successfully!"
            # The template will now display a success message

        # NOTE ON CORRECTION: If validation fails, the `form` variable already
        # contains the data and errors, so you just skip to the final render.
        # You DO NOT re-instantiate an empty form here.

    else:
        # 3. Initial GET request
        form = EmailPostForm()

    # Final render call, used for both initial GET, valid POST (success),
    # and invalid POST (display errors).
    return render(
        request,
        'blog/posts/share.html',
        {
            'post': post,
            'form': form,
            'title': title,
            'sent': sent # Pass 'sent' status to the template
        }
    )
