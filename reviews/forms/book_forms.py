from django import forms

from reviews.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'isbn', 'cover')

class SearchForm(forms.Form):
    SEARCH_TYPE = (
        ("title", "Title"),
        ("publisher", "Publisher"),
    )

    search_book_by = forms.MultipleChoiceField(
        choices=SEARCH_TYPE,
        required=True,  # Explicitly make this field mandatory
        error_messages={"required": ""},
        widget=forms.CheckboxSelectMultiple,
        label="Search within:",  # Added label for clarity
    )
    search = forms.CharField(
        error_messages={"required": ""},
        widget=forms.TextInput(
            attrs={
                "type": "search",  # <--- This sets the input type to "search"
                "placeholder": "Enter your search term...",  # Optional
                "class": "form-control",  # Optional: For styling frameworks like Bootstrap
            }
        ),
    )

class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover']


