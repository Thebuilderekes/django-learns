
# views.py
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.views import login_required
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from reviews.forms.forms import NewsletterForm
from reviews.forms.book_forms import BookMediaForm, SearchForm, BookForm
from reviews.forms.review_forms import ReviewForm
from reviews.forms.publisher_forms import PublisherForm
from reviews.forms.review_forms import ReviewForm
from django.contrib import messages
from .models import Book, Review, Publisher, Contributor
from .utils import average_rating, create_edit_view


def home(request):
    welcome_message = "Welcome to the Book App"
    form = NewsletterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            print("valid form")
            # Retrieve total_sum calculated in form.clean()
        form = NewsletterForm(request.POST)
    else:
        form = NewsletterForm()

    context = {
        "message": welcome_message,
        "form": form,
    }
    return render(request, "reviews/index.html", context)

def is_authenticated_staff_user(user):
    """Check if user is authenticated and is a staff"""
    return user.is_authenticated and user.is_staff

def login(request):
    return render(request, "registration/login.html")

def profile(request):
    return render(request, "reviews/profile.html")

# --- Publisher create view ---
publisher_create_edit = create_edit_view(
    Publisher,
    PublisherForm,
    'reviews/create-publisher_form.html',
    'publisher_detail',
    obj_name_field='name'
)
#
publisher_create_edit = user_passes_test(is_authenticated_staff_user)(publisher_create_edit) #---applying

# --- Book create view ---
book_create_edit = create_edit_view(
    Book,
    BookForm,
    'reviews/create_book.html',
    'book_detail',
    obj_name_field='title'
)

book_create_edit = user_passes_test(is_authenticated_staff_user)(book_create_edit)

def publisher_list(request):
    """List all publishers."""
    publishers = Publisher.objects.all().order_by('name')
    return render(request, 'reviews/publisher-list.html', {
        'publishers': publishers
    })

def publisher_detail(request, pk):
    """Show publisher details."""
    publisher = get_object_or_404(Publisher, pk=pk)
    books = publisher.books.all()  # Using related_name='books'
    submit_text = "Edit publisher"

    return render(request, 'reviews/publisher-detail.html', {
        'publisher': publisher,
        'books': books,
    'submit_text': submit_text
    })

def book_list(request):
    # Use prefetch_related to grab all reviews at once
    # Use select_related to grab the publisher (Foreign Key) in the same query
    books = Book.objects.select_related('publisher').prefetch_related('reviews')

    title = "List of all books"
    count = books.count()
    book_list = []

    for book in books:
        # This no longer hits the database; it uses the prefetched data
        reviews = book.reviews.all()

        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0

        book_list.append({
            "book": book,
            "book_rating": book_rating,
            "number_of_reviews": number_of_reviews,
        })

    context = {"book_list": book_list, "title": title, "count": count}
    return render(request, "reviews/book-list.html", context)



def book_search(request):
    title = "search and review book"
    form = SearchForm(request.POST)
    context = {'form': form, "title": title}
    return render(request, "reviews/book-search_form.html", context)


def search_result(request):
    title = "Search results for books"
    search_term = ""
    form = SearchForm(request.GET)
    books_list = Book.objects.none()

    if form.is_valid():
        data = form.cleaned_data
        query = data.get('search', '').strip()
        search_fields = data.get('search_book_by', [])

        if query and search_fields:
            search_term = query

            # Build dynamic Q object for all search conditions
            q_objects = Q()

            for field_name in search_fields:
                if field_name == 'title':
                    q_objects = q_objects | Q(title__icontains=query)


                elif field_name == 'publisher':
                    q_objects |= Q(publisher__name__icontains=query)


            # Single optimized query with all joins
            books_list = (
                Book.objects
                .filter(q_objects)
                .select_related('publisher')  # Join publisher table
                .prefetch_related('contributors')  # Efficiently load contributors
                .distinct()  # Remove duplicates from many-to-many
            )
        else:
            search_term = "Please enter a search term and select search criteria"

    context = {
        "title": title,
        'search_term': search_term,
        "form": form,
        "books_results": books_list
    }
    return render(request, "reviews/book-search_form.html", context)

def book_detail(request, pk):
    """view to display the review detail of a book"""
    book = get_object_or_404(Book, pk=pk)
    title = f"Details of {book.title}"

    reviews = Review.objects.filter(book=book)
    # Alternative
    # reviews = book.reviews.all()  # type: ignore[attr-defined]
# Handle Review Submission
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login') # Or handle as you wish

        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.book = book
                review.creator = request.user
                review.save()
                messages.success(request, "Review posted!")
                return redirect('book_detail', pk=pk)
            except IntegrityError:
                # This catches the "Duplicate" error from the database
                messages.error(request, "You have already reviewed this book.")
                return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "title": title,
            'form': form,
            "book_rating": book_rating,
            "reviews": reviews,
        }
    else:
        context = {"book": book, "book_rating": None, "reviews": None, "title": title}
    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get('viewed_books', [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
            viewed_books.insert(0, viewed_book)
            viewed_books = viewed_books[:max_viewed_books_length]
            request.session['viewed_books'] = viewed_books
    return render(request, "reviews/book-detail.html", context)

def book_media(request, pk):
    instance = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            # Save but don't commit to DB yet
            book = form.save(commit=False)
            cover = form.cleaned_data.get('cover')

            if cover:
                # Open image using PIL
                image = Image.open(cover)
                image.thumbnail((300, 300))

                # Save the processed image to a BytesIO object
                temp_handle = io.BytesIO()
                # Use the original format (JPEG/PNG)
                image_format = image.format if image.format else 'JPEG'
                image.save(temp_handle, format=image_format)
                temp_handle.seek(0)

                # Save back to the cover field
                book.cover.save(cover.name, ContentFile(temp_handle.read()), save=False)

            book.save()
            messages.success(request, f'Book "{book.title}" was successfully updated.')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookMediaForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
        'model_type': 'Book',
        'is_file_upload': True
    }
    return render(request, 'reviews/instance-form.html', context)


@login_required
def review_edit(request, book_pk, review_pk):
    book = get_object_or_404(Book, pk=book_pk)
    # Ensure the review exists AND belongs to this specific book
    review = get_object_or_404(Review, pk=review_pk, book=book)

    # Permission Check: Only the creator or a staff member can edit
    if request.user != review.creator and not request.user.is_staff:
        raise PermissionDenied("You are not allowed to edit this review.")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated.")
            return redirect('book_detail', pk=book.pk)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'book': book,
        'review': review,
        'title': f'Editing review for {book.title}'
    }
    return render(request, 'reviews/review-edit.html', context)
