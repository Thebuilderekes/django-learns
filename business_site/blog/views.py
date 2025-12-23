from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from blog.models import Post
from business_site.settings import POSTS_PER_PAGE
from .forms import CommentForm, EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE  # Thsi becomes the page.paginator.num_pages
    template_name = "blog/posts/post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/posts/post_detail.html'
    context_object_name = 'post'  # This ensures the template uses 'post'

    def get_object(self, queryset=None):
        # Only return the Post object here
        return get_object_or_404(
            Post,
            publish_date__year=self.kwargs.get('year'),
            publish_date__month=self.kwargs.get('month'),
            publish_date__day=self.kwargs.get('day'),
            slug=self.kwargs.get('post'),
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        # Add your extra data to the context
        post = self.object  # The object returned by get_object()
        context['comments'] = post.comments.filter(active=True)
        context['form'] = CommentForm()

        return context
    # 4. Override get_object to handle the complex lookup


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
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            messages.success(request, " Your recommendation was sent successfully!")
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
            return redirect('blog:post_share', post_id=post.id)
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/posts/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent,
            'title': f"Recommend \"{post.title}\" by sharing to email"
        }
    )

@require_POST
def post_comment(request, post_id):
    """
    Handle the submission of a comment on a post.
    """
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # Create Comment object but don't save to DB yet
        comment = form.save(commit=False)
        # Assign the current post to the comment
        comment.post = post
        # Save to DB
        comment.save()

    # If form is invalid, it will still render with errors
    return render(
        request,
        'blog/posts/post_comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )
# -----
# def post_share(request, post_id):
#     """
#     Handles the sharing of a blog post via email.
#
#     This view performs the following steps:
#     1. Retrieves the published Post object based on the provided post_id.
#     2. If the request method is POST (form submission):
#        a. Validates the submitted data using EmailPostForm.
#        b. If valid, extracts data, composes the email, and sends it.
#        c. Renders the 'share' template with a success message (or handles the email failure).
#        d. If invalid, re-renders the 'share' template with the form populated
#           with submitted data and validation errors.
#     3. If the request method is GET (initial load):
#        a. Instantiates a blank EmailPostForm.
#        b. Renders the 'share' template with the post and the blank form.
#     """
#     # 1. Retrieve the post
#     # Note: Assuming 'Post' and 'EmailPostForm' are correctly imported.
#     post = get_object_or_404(
#         Post,
#         id=post_id,
#         status=Post.Status.PUBLISHED # Ensure only published posts can be shared
#     )
#     sent = False # Flag to indicate if email was sent successfully
#     title = f"Share \"{post.title}\" by email"  #page title
#
#     if request.method == 'POST':
#         # 2. Form was submitted
#         form = EmailPostForm(request.POST)
#
#         if form.is_valid():
#             # 2a. Form fields passed validation
#             cd = form.cleaned_data
#
#             # Build the URL for the post (Assuming canonical URL is used)
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#
#             # Compose the email
#             subject = f"{cd['name']} recommends you read {post.title}"
#             message = (
#                 f"Read {post.title} at {post_url}\n\n"
#                 f"{cd['name']}'s comments: {cd['comments']}"
#             )
#
#             # 2b. Send email
#             send_mail(subject, message, cd['email'], [cd['to']], fail_silently=False)
#             sent = "Message sent successfully!"
#             # The template will now display a success message
#
#         # NOTE ON CORRECTION: If validation fails, the `form` variable already
#         # contains the data and errors, so you just skip to the final render.
#         # You DO NOT re-instantiate an empty form here.
#
#     else:
#         # 3. Initial GET request
#         form = EmailPostForm()
#
#     # Final render call, used for both initial GET, valid POST (success),
#     # and invalid POST (display errors).
#     return render(
#         request,
#         'blog/posts/share.html',
#         {
#             'post': post,
#             'form': form,
#             'title': title,
#             'sent': sent # Pass 'sent' status to the template
#         }
#     )
#
# @require_POST
# def post_comment(request, post_id):
#
#     post = get_object_or_404(
#         Post,
#         id=post_id,
#         status=Post.Status.PUBLISHED # Ensure only published posts can be shared
#     )
#     comment = None
#     form  = CommentForm(data=request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.save()
#         return render(
#             request,
#             'blog/posts/post_comment.html',
#             {
#                 'post': post,
#                 'form': form,
#                 'comment': comment
#             }
#         )
