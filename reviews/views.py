# views.py
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from reviews.forms.forms import NewsletterForm, OrderForm
from reviews.forms.book_forms import SearchForm, BookForm
from reviews.forms.publisher_forms import PublisherForm
from reviews.forms.review_forms import ReviewForm
from django.contrib import messages
from .models import Book, Review, Publisher
from .utils import average_rating, create_edit_view


def home(request):
    welcome_message = "Welcome to the Book App"
    newsletterForm = NewsletterForm(request.POST or None)
    form = OrderForm(request.POST or None)

    total_sum = None

    if request.method == "POST":
        if form.is_valid():
            print("valid form")
            # Retrieve total_sum calculated in form.clean()
            total_sum = form.cleaned_data.get("total_sum")
    else:
        form = OrderForm()

    context = {
        "message": welcome_message,
        "form": newsletterForm,
        "order_form": form,
        "total_sum": total_sum,
    }
    return render(request, "reviews/index.html", context)
# views.py
publisher_create_edit = create_edit_view(
    Publisher,
    PublisherForm,
    'reviews/create-publisher_form.html',
    'publisher_detail',
    obj_name_field='name'
)

# --- Book Views ---
book_create_edit = create_edit_view(
    Book,
    BookForm,
    'reviews/create-Book_form.html',
    'book_detail',
    obj_name_field='title'
)
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

                elif field_name == 'isbn':
                    q_objects |= Q(isbn__icontains=query)

                elif field_name == 'publisher':
                    q_objects |= Q(publisher__name__icontains=query)

                elif field_name == 'contributor':
                    q_objects |= (
                        Q(contributors__first_names__icontains=query) |
                        Q(contributors__last_names__icontains=query)
                    )

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

def book_list(request):
    """View to list all books in the database with their details"""
    books = Book.objects.all()
    title = "List of all books"
    count = len(books)
    book_list = []
    for book in books:
        reviews = Review.objects.filter(book=book)

        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append(
            {
                "book": book,
                "book_pub": book.publisher,
                "book_pub_date": book.publication_date,
                "book_rating": book_rating,
                "number_of_reviews": number_of_reviews,
            }
        )
    context = {"book_list": book_list, "title": title, "count": count}

    # Render the HTML template, passing the context
    return render(request, "reviews/books.html", context)




def book_detail(request, pk):
    """view to display the review detail of a book"""
    book = get_object_or_404(Book, pk=pk)
    title = f"Details of {book.title}"

    reviews = Review.objects.filter(book=book)
    # Alternative
    # reviews = book.reviews.all()  # type: ignore[attr-defined]

    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "title": title,
            "book_rating": book_rating,
            "reviews": reviews,
        }
    else:
        context = {"book": book, "book_rating": None, "reviews": None, "title": title}
    return render(request, "reviews/book-detail.html", context)


def post_review(request):
    """This view is for testing only"""
    return render(request, "reviews/post_review.html")


