from django import forms


class SearchForm(forms.Form):
    SEARCH_TYPE = (
        ("title", "Title"),
        ("contributor", "Contributor Name"),
        ("publisher", "Publisher Name"),
        ("isbn", "ISBN (Exact Match)"),  # Added ISBN for precise search
    )

    search_book_by = forms.MultipleChoiceField(
        choices=SEARCH_TYPE,
        required=True,  # Explicitly make this field mandatory
        error_messages={"required": "Please select at least one field to search by."},
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


class NewsletterForm(forms.Form):
    signup = forms.BooleanField(
        label="Would you like to sign up for our newsletter?",
        required=False,
        label_suffix="",
    )
    email = forms.EmailField(
        help_text="Enter your email address to subscribe", required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If form has data and signup is checked, make email required
        if self.data.get("signup"):
            self.fields["email"].required = True

    def clean(self):
        cleaned_data = super().clean()
        signup = cleaned_data.get("signup")
        email = cleaned_data.get("email")

        if signup and not email:
            self.add_error(
                "email", "Email is required when signing up for the newsletter."
            )

        return cleaned_data


class OrderForm(forms.Form):

    itemA = forms.IntegerField(min_value=0, max_value=100, label="enter number 1")
    itemB = forms.IntegerField(min_value=0, max_value=100, label="enter number 2")

    def clean(self):
        cleaned_data = super().clean()
        itemA_value = cleaned_data.get("itemA")
        itemB_value = cleaned_data.get("itemB")


        # 3. Check if both values exist before performing the math.
        # If a field failed its initial validation (e.g., user entered 'abc'),
        # its value won't be in cleaned_data, and we should stop.
        if itemA_value is not None and itemB_value is not None:
            total_sum = itemA_value + itemB_value

            # 4. Apply the custom validation rule
            if total_sum > 100:
                # Add a non-field error (appears at the top of the form)
                self.add_error(
                    None,
                    f"The total quantity of Item A ({itemA_value}) and Item B ({itemB_value}) "
                    f"is {total_sum}, which exceeds the maximum allowed total of 100.",
                )

            # Optional: Store the result for later use (e.g., in the view)
            cleaned_data["itemA_value"] = 

            print("this is cleaned data", cleaned_data)
        # 5. Always return the full set of cleaned data
        return cleaned_data
