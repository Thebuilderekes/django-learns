from django.shortcuts import render, get_object_or_404
from .models import Book
from .utils import average_rating

# views.py


def home(request):
    title = "Welcome to the Book App"
    context = {"title ":title }
    return render(request, "reviews/index.html", context)

def book_search(request):
    title = "search results for books"
    search_text = request.GET.get("search", "")
    context = {"title":title, "search_text": search_text}
    return render(request, "reviews/book-search.html", context)



def book_list(request):
    """View to list all books in the database with their details"""
    books = Book.objects.all()
    title = "List of all books"
    book_list = []
    for book in books:
        reviews = book.review_set.all()

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
    context = {"book_list": book_list, "title": title}

    # Render the HTML template, passing the context
    return render(request, "reviews/books.html", context)

def book_detail(request, pk):
    """view to display the review detail of a book"""
    book = get_object_or_404(Book, pk=pk)
    title = f"Details of {book.title}"
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None,
            "title":title
        }
    return render(request, "reviews/book-detail.html", context)

def test_page(request):
    """This view is for testing only"""
    return render(request, 'testing.html')
