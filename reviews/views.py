# views.py
from django.urls import reverse # Import reverse at the top of your views.py
from django.db.models import Q # Needed for combining filters with OR logic
from django.shortcuts import get_object_or_404, render, redirect
from reviews.forms.forms import SearchForm, NewsletterForm, OrderForm, PublisherForm
from django.contrib import messages
from .models import Book, Review, Publisher
from .utils import average_rating


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
        print("form errors", form.errors)

    context = {
        "message": welcome_message,
        "form": newsletterForm,
        "order_form": form,
        "total_sum": total_sum,
    }
    return render(request, "reviews/index.html", context)

def publisher_edit(request, pk=None):
    # 1. Handle object retrieval for editing or initialize for creating
    if pk:
        # EDIT case: Retrieve existing Publisher object
        publisher_instance = get_object_or_404(Publisher, pk=pk)
        is_creating = False
        is_updating = True
    else:
        # CREATE case: No pk provided, so initialize to None
        publisher_instance = None
        is_creating = True

        form = PublisherForm(request.POST, instance=publisher_instance)
    # 2. Handle POST request (Form submission)
    if request.method == "POST":
        # Create a Form instance, using request.POST data
        # If editing (publisher_instance is not None), pass the instance for binding
        form = PublisherForm(request.POST, instance=publisher_instance)

        if form.is_valid():
            updated_publisher = form.save()

            # Set appropriate success message
            action = "created" if is_creating else "updated"
            messages.success(request, f"Publisher {updated_publisher} was successfully {action}.")
# 1. Get the base URL path for the creation route
            base_url = reverse('publisher_create')

            # 2. Manually construct the full URL with query parameters
            # Use f-strings for clear construction
            full_url = f"{base_url}?success=true&action={action}&pk={updated_publisher.pk}"

            # 3. Redirect the user to the fully constructed URL
            return redirect(full_url)
            # Redirect to the edit view of the newly created/updated object
#            return redirect("publisher_edit", pk=updated_publisher.pk)

    # 3. Handle GET request (Initial page load)
    else:
        # Create a Form instance, unbound if creating, or bound with
        # the existing instance data if editing.
        form = PublisherForm(instance=publisher_instance)

    # 4. Render the template with the form
    # The original code had the wrong parameters and a hardcoded success template.
    # It should render the template containing the form.
#         return render("request", "reviews/success.html",  {"form": form})
        success_message = None
        if request.GET.get('success') == 'true':
                action = request.GET.get('action', 'saved')
                pk = request.GET.get('pk')
                success_message = f"Publisher ID {pk} was successfully {action}."

            # 4. Render the template with the form and the message
        return render(
                request,
                "reviews/publisher-form.html",
                {
                    "form": form,
                    "success_message": success_message, # Pass the message to the template
                }
            )
#

def book_search(request):
    title = "search and review book"
    form = SearchForm(request.POST)
    context = {'form': form, "title": title}
    return render(request, "reviews/book-search.html", context)


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
        # reviews = book.reviews.all()  # type: ignore[attr-defined]

        # The expression reviews = book.review_set.all() works because of Django's automatic reverse relationship lookup for ForeignKey fields.

        # Since your Review model has a ForeignKey pointing to the Book model, Django automatically gives the Book object a property to access all related Review objects.
        # This establishes a one-to-many relationship: one Book can have many Review objects. The Review model is on the "many" side and holds the foreign key.

        # 2. Django Creates the Reverse Manager

        # Because the Review model has a ForeignKey pointing to Book, Django automatically creates a reverse relationship manager on the Book model instances.

        #   By default, this manager is named using the lowercase name of the related model (Review) followed by _set.

        #   Therefore, an instance of the Book model (book) gains a property called review_set.

        # If you wanted to rename this manager for clarity (e.g., to avoid the default _set name), you could define a related_name on the ForeignKey field in the Review model:

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


def create_review(request):
    if request.method == 'POST':

        form = CreateReview(request.POST)
        if form.is_valid():
            print("this its the type of form", type(form))
            for name, value in form.cleaned_data.items():
                print("this is name from form.cleaned data", "this is name:", name, "this is value:", value)
                print("{}: {}".format(name, type(value), value))
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = CreateReview()
    return render(
        request, "reviews/create_review.html", {"method": request.method, "form": form}
    )
